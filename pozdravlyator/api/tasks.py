# -*- coding: utf-8 -*-
"""
Фоновая задача рендеринга.

Запускается через FastAPI BackgroundTasks (поток из пула).
Создаёт собственную DB-сессию — нельзя переиспользовать сессию из запроса,
она уже закрыта к моменту выполнения фонового кода.
"""
import sys
import subprocess
from pathlib import Path

from .database import SessionLocal
from .models import Job

PYTHON       = sys.executable
RENDER_SCRIPT = str(Path(__file__).parent.parent / "render_video.py")


def render_job(job_id: str) -> None:
    db = SessionLocal()
    job: Job | None = None
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return

        job.status = "processing"
        db.commit()

        # собираем список фото в том порядке, в котором они были загружены (имена: 000.jpg, 001.jpg …)
        photos_dir = Path(job.photos_dir)
        photo_paths = sorted(
            p for p in photos_dir.iterdir()
            if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".heic", ".heif"}
        )
        if not photo_paths:
            raise RuntimeError("В папке нет фотографий")

        output_path = str(Path(job.output_path or "") or
                          Path(__file__).parent.parent / "output" / f"{job_id}.mp4")
        # если output_path ещё не задан — вычислим
        if not job.output_path:
            output_path = str(Path(__file__).parent.parent / "output" / f"{job_id}.mp4")

        cmd = [
            PYTHON, "-X", "utf8", RENDER_SCRIPT,
            "--photos", *[str(p) for p in photo_paths],
            "--audio",  job.audio_path,
            "--text",   job.text,
            "--mode",   job.mode,
            "--output", output_path,
        ]
        if job.watermark:
            cmd.append("--watermark")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        if result.returncode == 0:
            job.status = "done"
            job.output_path = output_path
        else:
            job.status = "error"
            job.error_message = (result.stderr or result.stdout or "Неизвестная ошибка")[-800:]

    except Exception as exc:
        if job:
            job.status = "error"
            job.error_message = str(exc)[:800]
    finally:
        db.commit()
        db.close()
