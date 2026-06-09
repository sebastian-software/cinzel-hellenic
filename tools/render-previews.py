#!/usr/bin/env python3
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "previews"
ORIGINAL_TTF = ROOT / "fonts" / "reference" / "Cinzel-Regular.ttf"
CURRENT_TTF = ROOT / "fonts" / "ttf" / "CinzelHellenic-Regular.ttf"
ARIAL = Path("/System/Library/Fonts/Supplemental/Arial.ttf")

PAPER = (251, 250, 246)
INK = (32, 36, 40)
MUTED = (99, 112, 122)
LINE = (220, 216, 207)
SOFT_LINE = (232, 229, 220)
WHITE = (255, 255, 255)


def font(path, size):
    return ImageFont.truetype(str(path), size=size)


def draw_text(draw, xy, text, selected_font, fill=INK, anchor=None):
    draw.text(xy, text, font=selected_font, fill=fill, anchor=anchor)


def text_width(draw, text, selected_font):
    left, _, right, _ = draw.textbbox((0, 0), text, font=selected_font)
    return right - left


def fit_font(path, text, max_width, start=112, minimum=78):
    draw = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    for size in range(start, minimum - 1, -2):
        selected_font = font(path, size)
        if text_width(draw, text, selected_font) <= max_width:
            return selected_font
    return font(path, minimum)


def center_glyph(draw, x, y, width, height, glyph, selected_font):
    left, top, right, bottom = draw.textbbox((0, 0), glyph, font=selected_font)
    text_w = right - left
    text_h = bottom - top
    draw_text(
        draw,
        (x + width / 2 - (left + text_w / 2), y + height / 2 - (top + text_h / 2) - 2),
        glyph,
        selected_font,
    )


def require_fonts():
    missing = [path for path in (ORIGINAL_TTF, CURRENT_TTF, ARIAL) if not path.exists()]
    if missing:
        formatted = "\n".join(f"- {path}" for path in missing)
        raise SystemExit(f"Missing required font file(s):\n{formatted}")


def render_specimen():
    title_font = font(ARIAL, 31)
    label_font = font(ARIAL, 27)
    small_font = font(ARIAL, 21)
    caption_font = font(ARIAL, 20)
    original_word = font(ORIGINAL_TTF, 118)
    current_word = font(CURRENT_TTF, 118)
    original_glyph = font(ORIGINAL_TTF, 92)
    current_glyph = font(CURRENT_TTF, 92)

    image = Image.new("RGB", (2100, 1380), PAPER)
    draw = ImageDraw.Draw(image)

    draw_text(draw, (70, 49), "Cinzel Hellenic Preview - Original vs Current Regular", title_font)
    draw.line((70, 98, 2030, 98), fill=LINE, width=2)

    sections = [
        ("PALAMEDES", "PALAMEDES", 128, 245, 370, 420),
        ("TERMINARO", "TERMINARO", 438, 555, 680, 735),
        ("Display sample", "ATHENA AEGIS ELEKTRA", 753, 875, 1000, 1060),
    ]

    for label, sample, top, original_base, current_base, divider in sections:
        draw_text(draw, (70, top + 72), label, label_font, MUTED)
        draw_text(draw, (305, top + 10), "Original", small_font, MUTED)
        draw_text(draw, (305, top + 138), "Current", small_font, MUTED)
        original_font = original_word
        current_font = current_word
        if sample == "ATHENA AEGIS ELEKTRA":
            original_font = fit_font(ORIGINAL_TTF, sample, 1700, 108, 80)
            current_font = fit_font(CURRENT_TTF, sample, 1700, 108, 80)
        draw_text(draw, (455, original_base), sample, original_font, anchor="ls")
        draw_text(draw, (455, current_base), sample, current_font, anchor="ls")
        draw.line((70, divider, 2030, divider), fill=SOFT_LINE, width=1)

    glyph_y = 1092
    draw_text(draw, (70, glyph_y + 48), "Changed glyphs", label_font, MUTED)
    draw_text(draw, (305, glyph_y + 10), "Original", small_font, MUTED)
    draw_text(draw, (305, glyph_y + 126), "Current", small_font, MUTED)

    for index, glyph in enumerate(["A", "E", "M", "O"]):
        x = 455 + index * 220
        for row, selected_font in enumerate([original_glyph, current_glyph]):
            y = glyph_y + row * 122
            draw.rectangle((x, y, x + 150, y + 116), outline=LINE, fill=WHITE)
            center_glyph(draw, x, y, 150, 116, glyph, selected_font)
        draw_text(draw, (x + 75, glyph_y + 256), glyph, caption_font, MUTED, anchor="mm")

    image.save(OUT / "specimen.png")


def render_e_detail():
    image = Image.new("RGB", (1280, 760), PAPER)
    draw = ImageDraw.Draw(image)
    title_font = font(ARIAL, 31)
    label_font = font(ARIAL, 27)

    draw_text(draw, (52, 42), "E detail - Original vs Current", title_font)
    draw.line((52, 92, 1228, 92), fill=LINE, width=2)
    draw_text(draw, (120, 154), "Original", label_font, MUTED)
    draw_text(draw, (670, 154), "Current", label_font, MUTED)
    draw_text(draw, (120, 262), "E", font(ORIGINAL_TTF, 420))
    draw_text(draw, (700, 262), "E", font(CURRENT_TTF, 420))
    image.save(OUT / "e-detail.png")


def render_overlay():
    image = Image.new("RGB", (2240, 760), PAPER)
    draw = ImageDraw.Draw(image)
    title_font = font(ARIAL, 31)
    label_font = font(ARIAL, 27)

    draw_text(draw, (52, 42), "A/E/M/O overlay - Original blue, Current red", title_font)
    draw.line((52, 92, 2188, 92), fill=LINE, width=2)

    for index, glyph in enumerate(["A", "E", "M", "O"]):
        x = 155 + index * 520
        draw_text(draw, (x, 165), glyph, label_font, MUTED)
        overlay = Image.new("RGBA", (500, 520), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.text((40, 60), glyph, font=font(ORIGINAL_TTF, 430), fill=(30, 90, 210, 105))
        overlay_draw.text((40, 60), glyph, font=font(CURRENT_TTF, 430), fill=(220, 50, 45, 135))
        image.paste(overlay, (x, 210), overlay)

    image.save(OUT / "ae-overlay.png")


def main():
    require_fonts()
    OUT.mkdir(parents=True, exist_ok=True)
    render_specimen()
    render_e_detail()
    render_overlay()
    print(f"Wrote previews to {OUT}")


if __name__ == "__main__":
    main()
