# -*- coding: utf-8 -*-
"""Generates test_assets/: 4 colored JPEGs + test_audio.wav (15 sec sine tone)."""
import os
import struct
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).parent / "test_assets"
OUT.mkdir(exist_ok=True)

# ── 4 test photos ───────────────────────────────────────────────────────────────
photos = [
    ((180, 90, 120),  "Photo 1"),
    ((80, 140, 200),  "Photo 2"),
    ((60, 170, 110),  "Photo 3"),
    ((220, 160, 50),  "Photo 4"),
]

for i, (color, label) in enumerate(photos, 1):
    img  = Image.new("RGB", (1200, 900), color)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 80)
    except OSError:
        font = ImageFont.load_default()
    draw.text((100, 100), label, fill=(255, 255, 255), font=font)
    out = OUT / f"photo{i}.jpg"
    img.save(str(out), "JPEG", quality=95)
    print(f"  {out}")

# ── 15-second WAV (440 Hz sine, 44100 Hz, mono, 16-bit) ───────────────────────
sample_rate = 44100
duration    = 15
freq        = 440
n_samples   = sample_rate * duration
amplitude   = 20000

wav_path = OUT / "test_audio.wav"
with open(wav_path, "wb") as f:
    # RIFF header
    data_size   = n_samples * 2          # 16-bit = 2 bytes per sample
    chunk_size  = 36 + data_size

    f.write(b"RIFF")
    f.write(struct.pack("<I", chunk_size))
    f.write(b"WAVE")

    # fmt chunk
    f.write(b"fmt ")
    f.write(struct.pack("<IHHIIHH",
        16,            # subchunk size
        1,             # PCM
        1,             # channels
        sample_rate,
        sample_rate * 2,
        2,             # block align
        16,            # bits per sample
    ))

    # data chunk
    f.write(b"data")
    f.write(struct.pack("<I", data_size))
    for i in range(n_samples):
        v = int(amplitude * math.sin(2 * math.pi * freq * i / sample_rate))
        f.write(struct.pack("<h", v))

print(f"  {wav_path}")
print("Done.")
