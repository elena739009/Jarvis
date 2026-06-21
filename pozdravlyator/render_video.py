# -*- coding: utf-8 -*-
"""
render_video.py -- ядро рендеринга Поздравлятора.

Использование:
    python render_video.py \
        --photos photo1.jpg photo2.jpg photo3.jpg \
        --audio  music.mp3 \
        --text   "С днём рождения, мама!" \
        --mode   scrolling|card \
        --output output/result.mp4 \
        [--watermark]

Зависимости: Pillow, imageio-ffmpeg  (pip install Pillow imageio-ffmpeg)
"""

import argparse
import os
import sys
import tempfile

# Принудительно UTF-8 для stdout/stderr — важно когда запускаемся как subprocess из API
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
import subprocess
from pathlib import Path

import imageio_ffmpeg
from PIL import Image
import numpy as np

# ─── пути ──────────────────────────────────────────────────────────────────────
FFMPEG_BIN     = imageio_ffmpeg.get_ffmpeg_exe()
FFPROBE_BIN    = str(Path(FFMPEG_BIN).parent / "ffprobe.exe")
if not Path(FFPROBE_BIN).exists():
    # imageio-ffmpeg иногда содержит только ffmpeg; используем его же для probe
    FFPROBE_BIN = FFMPEG_BIN.replace("ffmpeg-win", "ffprobe-win").replace("ffmpeg.exe", "ffprobe.exe")
    if not Path(FFPROBE_BIN).exists():
        FFPROBE_BIN = FFMPEG_BIN   # fallback: используем ffmpeg -i

ASSETS_DIR     = Path(__file__).parent / "assets"
WATERMARK_PATH = ASSETS_DIR / "watermark.png"

# ─── настройки видео ───────────────────────────────────────────────────────────
VIDEO_W      = 1920
VIDEO_H      = 1080
FPS          = 25
SCROLL_SPEED = 220        # px/сек для бегущей строки
CARD_SECONDS = 3.5        # сек финальной открытки


# ─── helpers ───────────────────────────────────────────────────────────────────

def find_font() -> str:
    """
    Копирует TTF-шрифт с кириллицей в assets/ и возвращает просто имя файла.
    Возвращает пустую строку если шрифт не найден.
    Используем только имя файла (без пути), чтобы избежать проблемы с 'C:'
    в filter-строке FFmpeg — ffmpeg будет запускаться с cwd=ASSETS_DIR.
    """
    local = ASSETS_DIR / "render_font.ttf"
    if local.exists():
        return local.name

    candidates = [
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\calibri.ttf",
        r"C:\Windows\Fonts\times.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    import shutil
    for p in candidates:
        if os.path.exists(p):
            shutil.copy2(p, str(local))
            return local.name
    return ""


def get_audio_duration(audio_path: str) -> float:
    """Длина аудио в секундах через ffmpeg -i (работает без ffprobe)."""
    result = subprocess.run(
        [FFMPEG_BIN, "-i", audio_path],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    # ffmpeg пишет длину в stderr: "Duration: HH:MM:SS.ms"
    import re
    m = re.search(r"Duration:\s*(\d+):(\d+):([\d.]+)", result.stderr)
    if m:
        h, mi, s = int(m.group(1)), int(m.group(2)), float(m.group(3))
        return h * 3600 + mi * 60 + s
    raise RuntimeError(f"Не удалось определить длину аудио: {audio_path}")


def load_and_fit(image_path: str) -> np.ndarray:
    """
    Загружает изображение, масштабирует contain → 1920×1080 на чёрном фоне.
    Возвращает numpy RGB-массив.
    """
    img = Image.open(image_path).convert("RGB")
    ratio = min(VIDEO_W / img.width, VIDEO_H / img.height)
    nw = int(img.width  * ratio)
    nh = int(img.height * ratio)
    img = img.resize((nw, nh), Image.LANCZOS)

    canvas = Image.new("RGB", (VIDEO_W, VIDEO_H), (0, 0, 0))
    canvas.paste(img, ((VIDEO_W - nw) // 2, (VIDEO_H - nh) // 2))
    return np.array(canvas)


def ffmpeg(*args, label: str = "", cwd: str = None) -> None:
    """Запускает FFmpeg, бросает RuntimeError при ошибке."""
    cmd = [FFMPEG_BIN, "-y"] + list(args)
    result = subprocess.run(
        cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=cwd
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"FFmpeg{' (' + label + ')' if label else ''} завершился с кодом {result.returncode}:\n"
            f"{result.stderr[-2000:]}"
        )


# ─── основной рендер ───────────────────────────────────────────────────────────

def build_video(
    photo_paths: list,
    audio_path:  str,
    text:        str,
    mode:        str,       # "scrolling" | "card"
    output_path: str,
    watermark:   bool = False,
) -> None:
    """
    Сборка MP4 через FFmpeg.

    Шаги:
      1. Масштабировать фото → временные PNG 1920×1080
      2. concat-слайдшоу + аудио → slideshow.mp4
      3. Наложить текст → with_text.mp4
      4. Наложить водяной знак (если нужно) → with_wm.mp4
      5. Финальный экспорт с faststart → output_path
    """
    audio_duration    = get_audio_duration(audio_path)
    n                 = len(photo_paths)
    dur_per_slide     = audio_duration / n
    font_path         = find_font()

    print(f"  Длина трека: {audio_duration:.1f} сек  |  {n} фото  |  {dur_per_slide:.1f} сек/слайд")

    with tempfile.TemporaryDirectory() as _tmp:
        tmp = Path(_tmp)

        # ── 1. подготовить кадры ──────────────────────────────────────────────
        frame_paths = []
        for i, ph in enumerate(photo_paths):
            arr   = load_and_fit(ph)
            out   = tmp / f"frame_{i:03d}.png"
            Image.fromarray(arr).save(str(out))
            frame_paths.append(str(out))

        # ── 2. concat → slideshow + audio ────────────────────────────────────
        concat_txt = tmp / "concat.txt"
        with open(concat_txt, "w", encoding="utf-8") as f:
            for fp in frame_paths:
                f.write(f"file '{fp}'\n")
                f.write(f"duration {dur_per_slide:.4f}\n")
            f.write(f"file '{frame_paths[-1]}'\n")   # повтор последнего (требование FFmpeg)

        slideshow = tmp / "slideshow.mp4"
        ffmpeg(
            "-f", "concat", "-safe", "0", "-i", str(concat_txt),
            "-i", audio_path,
            "-r", str(FPS),
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-c:a", "aac", "-b:a", "192k",
            "-pix_fmt", "yuv420p", "-shortest",
            str(slideshow),
            label="slideshow",
        )

        # ── 3. наложить текст ─────────────────────────────────────────────────
        # Текст в одинарных кавычках: внутри них ‘,’ и ‘:’ не нужно экранировать.
        # find_font() вернул просто имя файла (render_font.ttf) без drive-letter.
        # ffmpeg для drawtext запустим с cwd=ASSETS_DIR → шрифт найдётся по имени.
        safe = (text
                .replace("\\", "\\\\")
                .replace("’",  "’"))  # заменяем ASCII ‘ на типографский

        font_arg = f":fontfile={font_path}" if font_path else ""
        fsize    = 56

        if mode == "scrolling":
            vf = (
                f"drawtext=text='{safe}'"
                f"{font_arg}"
                f":fontsize={fsize}"
                f":fontcolor=white"
                f":shadowcolor=black:shadowx=3:shadowy=3"
                f":y=h-th-40"
                f":x=w-mod(t*{SCROLL_SPEED}\\,w+tw)"
            )
        else:  # card
            start = max(0.0, audio_duration - CARD_SECONDS)
            vf = (
                f"drawtext=text='{safe}'"
                f"{font_arg}"
                f":fontsize={fsize}"
                f":fontcolor=white"
                f":shadowcolor=black:shadowx=3:shadowy=3"
                f":x=(w-tw)/2:y=(h-th)/2"
                f":enable='gte(t,{start:.2f})'"
            )

        with_text = tmp / "with_text.mp4"
        ffmpeg(
            "-i", str(slideshow),
            "-vf", vf,
            "-c:v", "libx264", "-preset", "fast", "-crf", "21",
            "-c:a", "copy",
            str(with_text),
            label="drawtext",
            cwd=str(ASSETS_DIR),   # ffmpeg ищет шрифт относительно этой папки
        )

        # ── 4. водяной знак ───────────────────────────────────────────────────
        source = with_text
        if watermark and WATERMARK_PATH.exists():
            with_wm = tmp / "with_wm.mp4"
            ffmpeg(
                "-i", str(source),
                "-i", str(WATERMARK_PATH),
                "-filter_complex", "overlay=W-w-30:H-h-30",
                "-c:v", "libx264", "-preset", "fast", "-crf", "21",
                "-c:a", "copy",
                str(with_wm),
                label="watermark",
            )
            source = with_wm

        # ── 5. финальный экспорт ──────────────────────────────────────────────
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        ffmpeg(
            "-i", str(source),
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart",
            "-pix_fmt", "yuv420p",
            output_path,
            label="final",
        )

    print(f"[OK] Video ready: {output_path}")


# ─── CLI ───────────────────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(description="Pozdravlyator video renderer")
    p.add_argument("--photos",    nargs="+", required=True)
    p.add_argument("--audio",     required=True)
    p.add_argument("--text",      required=True)
    p.add_argument("--mode",      choices=["scrolling", "card"], default="scrolling")
    p.add_argument("--output",    default="output/result.mp4")
    p.add_argument("--watermark", action="store_true")
    return p.parse_args()


def main():
    args = parse_args()

    missing = [p for p in args.photos if not os.path.exists(p)]
    if missing:
        sys.exit(f"Photos not found: {missing}")
    if not os.path.exists(args.audio):
        sys.exit(f"Audio not found: {args.audio}")

    print(f"Photos:    {len(args.photos)}")
    print(f"Audio:     {args.audio}")
    print(f"Text:      {args.text}")
    print(f"Mode:      {args.mode}")
    print(f"Watermark: {args.watermark}")
    print(f"Output:    {args.output}")
    print("-" * 48)

    build_video(
        photo_paths=args.photos,
        audio_path=args.audio,
        text=args.text,
        mode=args.mode,
        output_path=args.output,
        watermark=args.watermark,
    )


if __name__ == "__main__":
    main()
