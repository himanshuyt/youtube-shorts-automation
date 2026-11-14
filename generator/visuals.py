from PIL import Image, ImageDraw, ImageFont
import textwrap
from pathlib import Path
from config.settings import VIDEO_WIDTH, VIDEO_HEIGHT

def _font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()

def render_scene(text, index, total, out_path, category):
    w, h = VIDEO_WIDTH, VIDEO_HEIGHT
    img = Image.new("RGB", (w, h), (10, 14, 28))
    draw = ImageDraw.Draw(img)
    # Original graphic treatment: layered gradients and geometric accents.
    for y in range(h):
        t = y / h
        color = (int(12 + 15*t), int(17 + 12*t), int(35 + 28*t))
        draw.line((0, y, w, y), fill=color)
    accent = (255, 190, 70) if category == "gta6" else (120, 190, 255)
    draw.rounded_rectangle((65, 110, w-65, 180), radius=28, fill=(30, 38, 58))
    label = "GTA VI • FACT CHECK" if category == "gta6" else "ORIGINAL SHORT STORY"
    draw.text((95, 128), label, font=_font(30, True), fill=accent)
    draw.ellipse((w-230, 250, w+80, 560), outline=accent, width=8)
    draw.ellipse((-130, h-500, 210, h-160), outline=(70, 90, 130), width=7)
    draw.rounded_rectangle((65, 560, w-65, 1360), radius=45, fill=(20, 27, 47), outline=(65, 78, 110), width=3)
    lines = textwrap.wrap(text, width=25)
    font = _font(54 if len(lines) < 5 else 46, True)
    line_heights = [draw.textbbox((0,0), line, font=font)[3] + 20 for line in lines]
    y = 960 - sum(line_heights)//2
    for line, line_h in zip(lines, line_heights):
        bbox = draw.textbbox((0,0), line, font=font)
        x = (w - (bbox[2]-bbox[0])) // 2
        draw.text((x, y), line, font=font, fill=(245, 247, 252))
        y += line_h
    draw.text((75, 1780), f"EPISODE {index+1:02d}  /  {total:02d}", font=_font(26), fill=(175, 185, 205))
    draw.text((w-300, 1780), "FOLLOW FOR MORE", font=_font(23, True), fill=accent)
    img.save(out_path, quality=95)
