"""Generates assets/watermark.png — run once after install."""
from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT = os.path.join(os.path.dirname(__file__), "assets", "watermark.png")

W, H = 420, 80

img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# rounded rect background
rx = 16
draw.rounded_rectangle([0, 0, W - 1, H - 1], radius=rx, fill=(10, 10, 10, 160))

# star symbol
draw.text((18, 14), "★", fill=(192, 132, 252, 230), font=None)

# text
try:
    font = ImageFont.truetype("arial.ttf", 28)
except OSError:
    font = ImageFont.load_default()

draw.text((52, 16), "Поздравлятор", fill=(255, 255, 255, 220), font=font)

img.save(OUTPUT, "PNG")
print(f"Watermark saved: {OUTPUT}")
