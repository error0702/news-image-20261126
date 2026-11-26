#!/usr/bin/env python3
"""Draw the 26 November 2026 front page: "The World in One Day".

A newspaper front page, 1024x1024, drawn entirely with Pillow shapes and
real fonts (DejaVu). No photos, no generated images, no network: every
headline is crisp rendered text. The layout flows top to bottom from a
running y cursor, so no block can overrun the one below it. Run from the
repository root:

    python3 build/render.py

and it writes entry.png next to main.ts.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 34

PAPER = (251, 247, 238)   # warm newsprint
INK = (24, 24, 22)        # near-black
RED = (163, 22, 33)       # kicker / rule accent
GREY = (92, 88, 80)       # secondary text

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines, current = [], ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    """Draw lines left-aligned starting at (x, y); return y after last."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def draw_globe(draw, cx, cy, r):
    """A small line-drawn globe: outline, meridians, parallels."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=2)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
                 outline=INK, width=1)
    draw.line([cx - r, cy, cx + r, cy], fill=INK, width=1)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
             start=200, end=340, fill=INK, width=1)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
             start=20, end=160, fill=INK, width=1)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = MARGIN + 14, W - MARGIN - 14

    # Double outer border, newspaper style.
    d.rectangle([26, 26, W - 26, H - 26], outline=INK, width=3)
    d.rectangle([32, 32, W - 32, H - 32], outline=INK, width=1)

    # ---- Masthead -------------------------------------------------------
    title = font(SERIF_BOLD, 60)
    d.text((W // 2, 46), "The World in One Day", font=title, fill=INK,
           anchor="ma")

    # Small globe tucked into the masthead's right corner, clear of the title.
    draw_globe(d, 930, 82, 23)

    d.line([x0, 126, x1, 126], fill=INK, width=2)
    date_font = font(SANS_BOLD, 21)
    d.text((W // 2, 136), "THURSDAY  ·  26 NOVEMBER 2026", font=date_font,
           fill=INK, anchor="ma")
    tag_font = font(SERIF, 18)
    d.text((W // 2, 164), "Six stories that defined the day, reported around the world",
           font=tag_font, fill=GREY, anchor="ma")
    d.line([x0, 194, x1, 194], fill=RED, width=3)
    d.line([x0, 199, x1, 199], fill=INK, width=1)

    # ---- Lead story: tariffs -------------------------------------------
    y = 212
    kicker = font(SANS_BOLD, 16)
    d.text((x0, y), "TRADE WAR  —  THE LEAD STORY", font=kicker, fill=RED)
    y += 26
    head = font(SERIF_BOLD, 36)
    y = draw_lines(d, wrap(d, "Trump opens a second act in the tariff war",
                           head, x1 - x0),
                   x0, y, head, INK, 44)
    y += 4
    stand = font(SANS, 20)
    y = draw_lines(d, wrap(d, "Washington proposes 25% duties on Indian goods "
                           "and fresh levies on China, Japan and the EU, "
                           "citing factory overcapacity — markets slide.",
                           stand, x1 - x0),
                   x0, y, stand, INK, 26)
    y += 12

    # ---- 2 x 2 grid of the day's other big stories ----------------------
    grid_top = y
    d.line([x0, grid_top, x1, grid_top], fill=INK, width=2)
    col_w = (x1 - x0 - 24) // 2
    mid_x = x0 + col_w + 12
    row_h = 176
    grid_bottom = grid_top + 2 * row_h
    d.line([mid_x, grid_top + 8, mid_x, grid_bottom - 8], fill=GREY, width=1)
    d.line([x0, grid_top + row_h, x1, grid_top + row_h], fill=GREY, width=1)

    stories = [
        ("MIDDLE EAST",
         "Houthis claim refinery strike as oil tops $94",
         "Yemen's Houthis say they hit Saudi Arabia's Ras Tanura refinery "
         "and Riyadh's financial district. Brent jumps 3.5% as Hormuz "
         "shipping stalls."),
        ("EGYPT",
         "Tanker fire kills 31 on Cairo ring road",
         "A fuel tanker overturns and bursts into flames on the capital's "
         "Ring Road, charring dozens of cars. Twenty-one are hurt and the "
         "toll may still rise."),
        ("NORTH KOREA",
         "Kim orders wider spread of tactical nuclear arms",
         "Kim Jong Un calls for tactical nuclear weapons to be deployed "
         "more widely, as Pyongyang expels Switzerland's top envoy in a "
         "sanctions row."),
        ("UKRAINE",
         "Ukraine hits Russian air base, damages five jets",
         "Kyiv says its strike on a major Russian air base damaged five "
         "aircraft, as dozens of states urge Moscow to halt the alleged "
         "use of a riot agent."),
    ]
    cell_head = font(SERIF_BOLD, 27)
    cell_stand = font(SANS, 17)
    cell_kicker = font(SANS_BOLD, 14)
    positions = [(x0, grid_top + 12), (mid_x + 12, grid_top + 12),
                 (x0, grid_top + row_h + 12),
                 (mid_x + 12, grid_top + row_h + 12)]
    for (kick, headline, body), (cx, cy) in zip(stories, positions):
        d.text((cx, cy), kick, font=cell_kicker, fill=RED)
        cy += 22
        cy = draw_lines(d, wrap(d, headline, cell_head, col_w - 12),
                        cx, cy, cell_head, INK, 32)
        cy += 4
        draw_lines(d, wrap(d, body, cell_stand, col_w - 12),
                   cx, cy, cell_stand, INK, 22)

    # ---- Culture band ----------------------------------------------------
    y = grid_bottom + 14
    d.line([x0, y, x1, y], fill=INK, width=2)
    y += 12
    d.text((x0, y), "CULTURE", font=cell_kicker, fill=RED)
    y += 22
    band_head = font(SERIF_BOLD, 29)
    d.text((x0, y), "Duran Duran guitarist Andy Taylor dies at 65",
           font=band_head, fill=INK)
    y += 38
    band_stand = font(SANS, 18)
    d.text((x0, y), "The new-wave band's original guitarist, behind "
           "\u201cHungry Like the Wolf\u201d and \u201cRio\u201d, was 65.",
           font=band_stand, fill=INK)
    y += 30

    # ---- Also today ------------------------------------------------------
    d.line([x0, y, x1, y], fill=GREY, width=1)
    y += 10
    d.text((x0, y), "ALSO TODAY", font=cell_kicker, fill=INK)
    y += 24
    also_font = font(SANS, 16)
    items = [
        "Six die in a plane crash off the southern US coast",
        "South Africa court voids the Ramaphosa impeachment report",
        "Record 2,000 migrants reach the Canary Islands in a day",
        "Second US judge blocks Trump's birthright citizenship order",
    ]
    for item in items:
        d.rectangle([x0, y + 5, x0 + 7, y + 12], fill=RED)
        d.text((x0 + 14, y), item, font=also_font, fill=INK)
        y += 21

    # ---- Footer ----------------------------------------------------------
    foot = font(SANS, 13)
    d.text((W // 2, 964), "All stories reported on Thursday 26 November 2026  ·  "
           "Drawn with Pillow — no photographs", font=foot, fill=GREY,
           anchor="ma")

    img.save("entry.png", optimize=True)
    print(f"wrote entry.png {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
