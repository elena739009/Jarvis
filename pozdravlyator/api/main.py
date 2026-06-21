# -*- coding: utf-8 -*-
"""
Поздравлятор — FastAPI backend (Этап 2–3).

Эндпоинты:
  GET  /               — веб-интерфейс (index.html)
  POST /jobs           — принять фото + аудио + параметры, запустить рендер
  GET  /jobs/{id}      — статус задачи и ссылка на видео
  GET  /files/{name}   — скачать готовое видео
  GET  /health         — проверка сервиса
  DELETE /jobs/cleanup — удалить просроченные задачи (ручной запуск)
"""
import shutil
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List

from fastapi import (
    BackgroundTasks, Depends, FastAPI, File, Form,
    HTTPException, Request, UploadFile,
)
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from .config import settings
from .database import Base, engine, get_db
from .models import Job
from .schemas import JobResponse, TextMode
from .tasks import render_job

# ── инициализация ──────────────────────────────────────────────────────────────
STATIC_DIR = Path(__file__).parent.parent / "static"

Base.metadata.create_all(bind=engine)
Path(settings.uploads_dir).mkdir(parents=True, exist_ok=True)
Path(settings.output_dir).mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="Поздравлятор API",
    version="0.3.0",
    description="Сервис создания видео-поздравлений из фото + аудио",
)

app.mount("/files",  StaticFiles(directory=settings.output_dir), name="files")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)),     name="static")

# ── допустимые типы файлов ─────────────────────────────────────────────────────
PHOTO_TYPES = {
    "image/jpeg", "image/jpg", "image/png",
    "image/heic", "image/heif",
}
AUDIO_TYPES = {
    "audio/mpeg", "audio/mp3", "audio/wav",
    "audio/x-wav", "audio/mp4", "audio/m4a",
    "audio/aac", "audio/ogg",
}


# ── helpers ────────────────────────────────────────────────────────────────────

def _utcnow():
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _job_to_response(job: Job, request: Request) -> JobResponse:
    output_url = None
    if job.status == "done" and job.output_path:
        filename = Path(job.output_path).name
        base = str(request.base_url).rstrip("/")
        output_url = f"{base}/files/{filename}"
    return JobResponse(
        id=job.id,
        status=job.status,
        text=job.text,
        mode=job.mode,
        watermark=job.watermark,
        output_url=output_url,
        error_message=job.error_message,
        created_at=job.created_at,
        expires_at=job.expires_at,
    )


# ── маршруты ──────────────────────────────────────────────────────────────────

@app.get("/", include_in_schema=False)
def index():
    return FileResponse(str(STATIC_DIR / "index.html"))


@app.post("/jobs", response_model=JobResponse, status_code=201,
          summary="Создать задачу рендеринга")
async def create_job(
    request:         Request,
    background_tasks: BackgroundTasks,
    photos: List[UploadFile] = File(...,  description="Фотографии JPEG/PNG/HEIC, до 30 шт."),
    audio:  UploadFile       = File(...,  description="Аудио MP3/WAV/M4A"),
    text:   str              = Form(...,  max_length=500, description="Текст поздравления"),
    mode:   TextMode         = Form(TextMode.scrolling, description="Стиль текста"),
    watermark: bool          = Form(True, description="Добавить водяной знак"),
    db: Session              = Depends(get_db),
):
    # rate limiting по IP
    ip = request.client.host
    since = _utcnow() - timedelta(hours=1)
    recent = db.query(Job).filter(Job.ip_address == ip, Job.created_at >= since).count()
    if recent >= settings.jobs_per_hour_limit:
        raise HTTPException(429, detail=f"Лимит: не более {settings.jobs_per_hour_limit} задач в час")

    # валидация количества
    if not photos:
        raise HTTPException(400, "Нужно хотя бы одно фото")
    if len(photos) > settings.max_photos:
        raise HTTPException(400, f"Максимум {settings.max_photos} фотографий")

    # валидация типов
    bad_photos = [p.filename for p in photos if p.content_type not in PHOTO_TYPES]
    if bad_photos:
        raise HTTPException(400, f"Недопустимый тип файла: {bad_photos[0]}")
    if audio.content_type not in AUDIO_TYPES:
        raise HTTPException(400, f"Недопустимый тип аудио: {audio.content_type}")

    # создаём директорию задачи
    job_id    = str(uuid.uuid4())
    job_dir   = Path(settings.uploads_dir) / job_id
    photos_dir = job_dir / "photos"
    photos_dir.mkdir(parents=True)

    try:
        # сохраняем фото
        for i, photo in enumerate(photos):
            content = await photo.read()
            if len(content) > settings.max_photo_mb * 1024 * 1024:
                raise HTTPException(400, f"{photo.filename}: файл > {settings.max_photo_mb} МБ")
            ext  = Path(photo.filename or "photo.jpg").suffix.lower() or ".jpg"
            dest = photos_dir / f"{i:03d}{ext}"
            dest.write_bytes(content)

        # сохраняем аудио
        audio_content = await audio.read()
        if len(audio_content) > settings.max_audio_mb * 1024 * 1024:
            raise HTTPException(400, f"Аудио > {settings.max_audio_mb} МБ")
        audio_ext  = Path(audio.filename or "audio.mp3").suffix.lower() or ".mp3"
        audio_path = str(job_dir / f"audio{audio_ext}")
        Path(audio_path).write_bytes(audio_content)

    except HTTPException:
        shutil.rmtree(job_dir, ignore_errors=True)
        raise

    # сохраняем Job в БД
    job = Job(
        id=job_id,
        text=text,
        mode=mode.value,
        watermark=watermark,
        photos_dir=str(photos_dir),
        audio_path=audio_path,
        ip_address=ip,
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    # запускаем рендер в фоне
    background_tasks.add_task(render_job, job_id)

    return _job_to_response(job, request)


@app.get("/jobs/{job_id}", response_model=JobResponse,
         summary="Статус задачи")
def get_job(job_id: str, request: Request, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(404, "Задача не найдена")
    return _job_to_response(job, request)


@app.delete("/jobs/cleanup", summary="Удалить просроченные задачи (ручной запуск)")
def cleanup_jobs(db: Session = Depends(get_db)):
    now     = _utcnow()
    expired = db.query(Job).filter(Job.expires_at < now).all()
    count   = 0
    for job in expired:
        # удаляем загруженные файлы
        if job.photos_dir:
            shutil.rmtree(Path(job.photos_dir).parent, ignore_errors=True)
        # удаляем выходное видео
        if job.output_path and Path(job.output_path).exists():
            Path(job.output_path).unlink(missing_ok=True)
        db.delete(job)
        count += 1
    db.commit()
    return {"deleted": count, "message": f"Удалено {count} просроченных задач"}


@app.get("/health", summary="Проверка сервиса")
def health():
    return {"status": "ok", "version": "0.2.0"}
