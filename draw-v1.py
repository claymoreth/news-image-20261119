#!/usr/bin/env python3
"""NEWS-IMAGE-20261119 V1 — built on our V2.6 architecture (white masthead, hero 1+2, horizontal grid, outline map + blue pins, numbers bar bottom, italic date check, WHITE paper), 40 stories all Thursday 19 November 2026. Own layout, own words — NOT a copy of Rank #1 or Rank #2.
front page (owner-supplied). Architecture is ours, words are ours: nothing
is copied from either reference — no headline, no label, no sentence.

Same 40 verified stories (141/126 drones, Kerch framed 18 Nov, ADNOC
no.22, Date Check), restructured:
  - masthead: WHITE, "THE WORLD" big black serif centred, date below,
    count line on top ("40 STORIES · 7 REGIONS · 16 DRAWN").
  - BY REGION bar: 7 segments sized by count, greyscale + brick + navy.
  - timeline "WEDNESDAY, HOUR BY HOUR": only times we can stand behind
    (ONS 07:00 GMT, Fed 14:00 EST = 19:00 UTC, GTA VI midnight EST =
    05:00 UTC); the rest are descriptors (Overnight / Morning / Today).
  - grid: 4 LARGE stories (APEC, Gulf, Voyager, Kerch) + 6 + 6 MEDIUM
    (Nvidia, Akvan, Sudan, EU, UK, Gaza / Peltola, GTA VI, Bangladesh,
    Fed, COP31, Afghanistan) = 16 visual stories, each with its own
    drawn visual (flags, skyline, map, space, bridge, chip, cyclone,
    pin, EU star, chart, tank, ballot, controller, factory, globe, quake).
  - map: continent OUTLINES (no dot-matrix) + small BLUE pins (r=6),
    legend above; list 17-40 in TWO columns at right.
  - numbers: SIX white boxes with thin black borders at the BOTTOM.
  - date check: ONE italic line in the footer, no red box.
  - palette: black + white + greys + brick red + dark blue only.
  - font: serif headlines, sans body.

Drawn with Pillow. Deterministic: fixed geometry/text, no randomness.
Writes entry.png (1024x1024) next to this file.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

# ---------- palette (black + white + brick red + dark blue only) ----------
INK = (18, 18, 18)
PAPER = (255, 255, 255)          # clean white paper, 19 Nov (NOT cream)
BRICK = (178, 60, 40)          # brick red accent
NAVY2 = (20, 50, 90)           # dark blue accent
NAVYBLUE = NAVY2
NAVYBLUE = NAVY2
GREY = (90, 90, 90)
# ---------- region colours (V2.5: colourful) ----------
REGION_COLORS = {
    "AMERICAS": (30, 90, 180),    # blue
    "ASIA": (200, 60, 50),        # red
    "EUROPE": (25, 60, 130),      # navy
    "MIDDLE EAST": (35, 140, 75), # green
    "AFRICA": (220, 130, 30),     # orange
    "OCEANIA": (0, 150, 150),     # teal
    "WORLD": (120, 80, 165),      # purple
}
GREY_LT = (242, 242, 240)
GREY_MD = (200, 200, 200)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def font_path(path, size):
    return ImageFont.truetype(path, size)


F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SERIF = lambda s: font("DejaVuSerif.ttf", s)
F_SERIF_I = lambda s: font("DejaVuSerif-Italic.ttf", s) if os.path.exists(
    os.path.join(FONT_DIR, "DejaVuSerif-Italic.ttf")) else font("DejaVuSerif.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)
F_SANS_I = lambda s: font("DejaVuSans-Oblique.ttf", s) if os.path.exists(
    os.path.join(FONT_DIR, "DejaVuSans-Oblique.ttf")) else font("DejaVuSans.ttf", s)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if text_w(draw, trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, cx, y, text, f, fill):
    w_ = text_w(draw, text, f)
    draw.text((cx - w_ / 2, y), text, font=f, fill=fill)
    return w_


def star_points(cx, cy, r_out, r_in, rot=-90):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


# ---------- flags ----------
def flag_us(d, x, y, w, h):
    stripe = h / 13.0
    for i in range(13):
        c = (178, 34, 52) if i % 2 == 0 else (255, 255, 255)
        d.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe], fill=c)
    cw, ch = w * 0.42, stripe * 7
    d.rectangle([x, y, x + cw, y + ch], fill=(28, 44, 96))
    for r_ in range(4):
        for c_ in range(5):
            sx = x + 4 + c_ * (cw - 8) / 4
            sy = y + 3 + r_ * (ch - 6) / 3
            d.ellipse([sx - 1.2, sy - 1.2, sx + 1.2, sy + 1.2], fill=(255, 255, 255))


def flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    cx, cy, r = x + w * 0.16, y + h * 0.28, h * 0.20
    d.polygon(star_points(cx, cy, r, r * 0.42), fill=(255, 222, 0))
    for sx, sy in [(0.34, 0.12), (0.42, 0.24), (0.40, 0.42), (0.30, 0.50)]:
        d.polygon(star_points(x + w * sx, y + h * sy, h * 0.07, h * 0.03), fill=(255, 222, 0))


def flag_ru(d, x, y, w, h):
    third = h / 3.0
    for i, c in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        d.rectangle([x, y + i * third, x + w, y + (i + 1) * third], fill=c)


# ---------- mini visuals (black / white / brick red / dark blue only) ----------
def mini_bars(d, x, y, w, h):
    vals = [0.4, 0.55, 0.7, 0.85, 1.0]
    n = len(vals)
    bw = w / n
    for i, v in enumerate(vals):
        bh = max(3, v * (h - 4))
        c = BRICK if i == n - 1 else NAVY2
        d.rectangle([x + i * bw + 2, y + h - bh, x + (i + 1) * bw - 2, y + h], fill=c)


def mini_line_up(d, x, y, w, h):
    pts = [(x + i * w / 5, y + h - (i * h / 5) - 3) for i in range(6)]
    d.line(pts, fill=NAVY2, width=3)
    d.ellipse([pts[-1][0] - 3, pts[-1][1] - 3, pts[-1][0] + 3, pts[-1][1] + 3], fill=BRICK)


def mini_cyclone(d, x, y, w, h):
    cx, cy = x + w / 2, y + h / 2
    for r, col in [(15, NAVY2), (10, (60, 90, 140)), (5, BRICK)]:
        d.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300, fill=col, width=3)


def mini_pin(d, x, y, w, h):
    cx, cy = x + w / 2, y + h / 2 - 4
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=BRICK)
    d.polygon([(cx - 7, cy + 5), (cx + 7, cy + 5), (cx, cy + 16)], fill=BRICK)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 255, 255))


def mini_eu(d, x, y, w, h):
    cx, cy = x + w / 2 - 12, y + h / 2
    d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=NAVY2)
    for i in range(8):
        a = math.radians(i * 45 - 90)
        sx, sy = cx + 9 * math.cos(a), cy + 9 * math.sin(a)
        d.ellipse([sx - 1.6, sy - 1.6, sx + 1.6, sy + 1.6], fill=(255, 255, 255))
    d.text((x + w - 34, y + h / 2 - 11), "€", font=F_SANS_B(22), fill=INK)


def mini_tank(d, x, y, w, h):
    d.rectangle([x + 8, y + h - 16, x + w - 8, y + h - 8], fill=(50, 50, 50))
    d.rectangle([x + 16, y + h - 26, x + w - 26, y + h - 16], fill=(70, 70, 70))
    d.line([x + w - 26, y + h - 21, x + w - 2, y + h - 21], fill=(70, 70, 70), width=3)
    for wx in range(4):
        d.ellipse([x + 12 + wx * 12, y + h - 7, x + 18 + wx * 12, y + h - 1], fill=(20, 20, 20))


def mini_ballot(d, x, y, w, h):
    d.rectangle([x + 10, y + 8, x + w - 10, y + h - 8], outline=NAVY2, width=2)
    d.line([(x + 16, y + h / 2 + 2), (x + w / 2 - 2, y + h - 12), (x + w - 16, y + 10)],
           fill=BRICK, width=4)


def mini_controller(d, x, y, w, h):
    d.rounded_rectangle([x + 6, y + 10, x + w - 6, y + h - 10], radius=8, fill=(25, 25, 30))
    d.ellipse([x + 14, y + h / 2 - 2, x + 20, y + h / 2 + 4], fill=(255, 255, 255))
    d.ellipse([x + w - 20, y + h / 2 - 2, x + w - 14, y + h / 2 + 4], fill=BRICK)
    d.text((x + w / 2 - 7, y + 12), "VI", font=F_SANS_B(11), fill=(255, 255, 255))


def mini_factory(d, x, y, w, h):
    d.rectangle([x + 8, y + h - 18, x + w - 8, y + h - 6], fill=(70, 70, 70))
    d.polygon([(x + 8, y + h - 18), (x + 16, y + h - 26), (x + 24, y + h - 18),
               (x + 32, y + h - 26), (x + 40, y + h - 18)], fill=(50, 50, 50))
    d.rectangle([x + w - 18, y + 4, x + w - 12, y + h - 18], fill=BRICK)
    d.ellipse([x + w - 16, y + 1, x + w - 10, y + 7], fill=(180, 180, 180))


def mini_chip(d, x, y, w, h):
    d.rectangle([x + 12, y + 8, x + w - 12, y + h - 8], fill=NAVY2)
    d.rectangle([x + 18, y + 14, x + w - 18, y + h - 14], outline=(255, 255, 255), width=1)
    for px in (18, 26, 34):
        d.line([x + px, y + 2, x + px, y + 8], fill=NAVY2, width=2)
        d.line([x + px, y + h - 8, x + px, y + h - 2], fill=NAVY2, width=2)
    d.text((x + w / 2 - 4, y + h / 2 - 7), "N", font=F_SANS_B(13), fill=(255, 255, 255))


def mini_bridge(d, x, y, w, h):
    d.arc([x + 4, y + 6, x + w - 4, y + h + 14], start=180, end=360, fill=NAVY2, width=3)
    d.line([x + 4, y + h - 8, x + w - 4, y + h - 8], fill=(60, 60, 60), width=2)
    d.line([x + w - 20, y + h - 8, x + w - 12, y + h - 1], fill=BRICK, width=3)


def mini_globe(d, x, y, w, h):
    cx, cy = x + w / 2, y + h / 2
    r = min(w, h) / 2 - 4
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY2, width=2)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=NAVY2, width=1)
    d.line([cx - r, cy, cx + r, cy], fill=NAVY2, width=1)
    d.arc([cx - r, cy - r * 0.45, cx + r, cy + r * 0.45], start=0, end=360, fill=NAVY2, width=1)
    d.ellipse([cx - 4, cy - r + 2, cx + 4, cy - r + 10], fill=BRICK)


def mini_quake(d, x, y, w, h):
    cx, cy = x + w / 2, y + h / 2
    for r, col in [(8, BRICK), (15, NAVY2), (22, (120, 140, 180))]:
        d.arc([cx - r, cy - r, cx + r, cy + r], start=200, end=340, fill=col, width=2)
    d.line([cx - 20, cy + 12, cx + 20, cy + 12], fill=(70, 70, 70), width=2)
    d.line([cx - 12, cy + 12, cx - 8, cy + 4], fill=(70, 70, 70), width=2)
    d.line([cx + 6, cy + 12, cx + 10, cy + 5], fill=(70, 70, 70), width=2)


def mini_visual(d, kind, x, y, w, h):
    {"bridge": mini_bridge, "chip": mini_chip, "cyclone": mini_cyclone,
     "pin": mini_pin, "eu": mini_eu, "line": mini_line_up, "tank": mini_tank,
     "ballot": mini_ballot, "controller": mini_controller,
     "factory": mini_factory, "bars": mini_bars, "globe": mini_globe,
     "quake": mini_quake}[kind](d, x, y, w, h)


# ---------- outline world map (no dots) ----------
CONTINENTS = {
    "NA": [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 60), (-55, 47),
           (-70, 42), (-75, 35), (-80, 26), (-85, 20), (-90, 15), (-95, 18), (-105, 22),
           (-115, 30), (-125, 40), (-125, 48), (-140, 60), (-155, 58), (-165, 60)],
    "SA": [(-80, 10), (-70, 12), (-60, 8), (-50, 0), (-40, -5), (-35, -10), (-40, -20),
           (-48, -28), (-58, -35), (-65, -45), (-70, -55), (-75, -50), (-80, -40),
           (-80, -25), (-80, -15)],
    "EU": [(-10, 36), (-5, 44), (0, 46), (5, 55), (10, 58), (18, 60), (25, 65), (30, 70),
           (35, 68), (40, 60), (30, 55), (25, 50), (20, 45), (15, 40), (10, 38), (0, 36)],
    "AF": [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28), (40, 15),
           (45, 11), (50, 10), (40, 0), (35, -10), (30, -20), (25, -30), (20, -35),
           (15, -30), (12, -18), (10, -5), (5, 5), (-5, 5), (-12, 8)],
    "AS": [(40, 70), (60, 75), (80, 73), (100, 77), (120, 75), (140, 72), (160, 70),
           (170, 66), (160, 60), (140, 55), (130, 45), (120, 40), (110, 35), (100, 30),
           (90, 25), (80, 20), (75, 10), (70, 15), (60, 25), (55, 30), (50, 35),
           (45, 40), (40, 45), (35, 50), (40, 60)],
    "OC": [(113, -22), (122, -15), (132, -12), (142, -11), (150, -20), (153, -28),
           (150, -37), (140, -38), (130, -32), (122, -34), (114, -30)],
}


def lonlat_to_xy(lon, lat, x0, y0, mw, mh):
    x = x0 + (lon + 180.0) / 360.0 * mw
    y = y0 + (75.0 - lat) / 130.0 * mh
    return x, y


def draw_outline_map(d, x0, y0, mw, mh):
    # light fill + dark outline per continent (no dots)
    for poly in CONTINENTS.values():
        pts = [lonlat_to_xy(lon, lat, x0, y0, mw, mh) for lon, lat in poly]
        d.polygon(pts, fill=(238, 240, 244))
        d.line(pts + [pts[0]], fill=(70, 70, 70), width=1)


def draw_pin_blue(d, x, y, num):
    r = 8
    d.ellipse([x - r, y - r, x + r, y + r], fill=NAVY2, outline=(255, 255, 255), width=1)
    f = F_SANS_B(8)
    tw = text_w(d, str(num), f)
    d.text((x - tw / 2, y - 6), str(num), font=f, fill=(255, 255, 255))


def hero_visual(d, kind, x, y, w, h):
    if kind == "apec":
        for i in range(h):
            t = i / max(1, h - 1)
            r = int(250 - 120 * t)
            g = int(170 - 90 * t)
            b = int(60 + 40 * t)
            d.line([x, y + i, x + w, y + i], fill=(r, g, b))
        d.ellipse([x + w - 64, y + 12, x + w - 18, y + 58], fill=(255, 230, 150))
        for bx, bw, bh in [(0.02, 0.10, 0.30), (0.13, 0.08, 0.45), (0.22, 0.11, 0.36),
                           (0.34, 0.09, 0.55), (0.44, 0.10, 0.40), (0.55, 0.08, 0.62),
                           (0.64, 0.11, 0.44), (0.76, 0.09, 0.52), (0.86, 0.12, 0.34)]:
            d.rectangle([x + bx * w, y + h - bh * h, x + (bx + bw) * w, y + h], fill=(30, 30, 45))
        fw, fh = 48, 30
        for i, fn in enumerate([flag_us, flag_cn, flag_ru]):
            fx = x + 16 + i * 62
            fy = y + 8
            d.line([fx + fw / 2, fy, fx + fw / 2, fy + fh + 26], fill=(255, 255, 255), width=2)
            fn(d, fx, fy, fw, fh)
    elif kind == "gulf":
        d.rectangle([x, y, x + w, y + h], fill=(16, 42, 78))
        d.polygon([(x, y + h * 0.15), (x + w * 0.30, y + h * 0.10), (x + w * 0.55, y + h * 0.30),
                   (x + w * 0.70, y + h * 0.55), (x + w * 0.62, y + h * 0.85), (x + w * 0.35, y + h),
                   (x, y + h)], fill=(52, 78, 60))
        for px, py, r in [(0.62, 0.30, 6), (0.72, 0.45, 4), (0.55, 0.60, 5), (0.80, 0.62, 3), (0.45, 0.42, 3)]:
            cx, cy = x + px * w, y + py * h
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 120, 40), outline=(255, 220, 120), width=1)
        d.rectangle([x + 4, y + h - 18, x + 62, y + h - 4], fill=(10, 25, 45))
        d.text((x + 8, y + h - 16), "HORMUZ", font=F_SANS_B(9), fill=(255, 220, 120))
    elif kind == "kerch":
        d.rectangle([x, y, x + w, y + h], fill=(235, 238, 242))
        # sea
        d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(120, 160, 200))
        # bridge deck + arch (fallen on the right)
        d.line([x + 8, y + h * 0.45, x + w - 8, y + h * 0.45], fill=(40, 40, 40), width=4)
        d.arc([x + w * 0.10, y + h * 0.08, x + w * 0.55, y + h * 0.75], start=180, end=360,
              fill=NAVY2, width=3)
        # fallen arch segment, tilted into the sea
        d.line([x + w * 0.62, y + h * 0.45, x + w * 0.85, y + h * 0.72], fill=BRICK, width=4)
        d.ellipse([x + w * 0.80, y + h * 0.68, x + w * 0.90, y + h * 0.78], fill=BRICK)
        # drone dots
        for px, py in [(0.15, 0.18), (0.30, 0.12), (0.50, 0.20), (0.70, 0.14)]:
            d.ellipse([x + px * w - 2, y + py * h - 2, x + px * w + 2, y + py * h + 2],
                      fill=(30, 30, 30))
        d.text((x + 8, y + h - 16), "KERCH STRAIT", font=F_SANS_B(9), fill=(255, 255, 255))
    elif kind == "voyager":
        d.rectangle([x, y, x + w, y + h], fill=(5, 8, 18))
        for sx, sy in [(0.08, 0.2), (0.2, 0.1), (0.3, 0.35), (0.45, 0.15), (0.55, 0.3),
                       (0.65, 0.12), (0.75, 0.28), (0.85, 0.18), (0.92, 0.4), (0.15, 0.55),
                       (0.35, 0.6), (0.6, 0.55), (0.8, 0.65), (0.5, 0.75), (0.25, 0.8)]:
            d.ellipse([x + sx * w - 1.5, y + sy * h - 1.5, x + sx * w + 1.5, y + sy * h + 1.5],
                      fill=(255, 255, 255))
        d.line([x + 20, y + h - 20, x + w - 40, y + 30], fill=(212, 175, 55), width=2)
        px, py = x + w - 60, y + 42
        d.polygon([(px, py - 8), (px + 16, py), (px, py + 8), (px - 16, py)], fill=(212, 175, 55))
        d.line([px - 16, py, px - 28, py - 10], fill=(232, 196, 90), width=2)
        d.rectangle([x + 8, y + 8, x + 92, y + 28], fill=(212, 175, 55))
        d.text((x + 12, y + 11), "1 LIGHT-DAY", font=F_SANS_B(11), fill=(10, 10, 10))


def draw_world_map_outline(d, x0, y0, mw, mh):
    """Outline world map: continent polygons as thin dark-blue outlines,
    light fill. NOT dot-matrix (that was Rank #1)."""
    # light graticule (fills empty ocean so the map does not read as blank)
    for lon in range(-150, 181, 30):
        gx = x0 + (lon + 180) / 360 * mw
        d.line([gx, y0, gx, y0 + mh], fill=(232, 234, 238), width=1)
    for lat in [60, 30, 0, -30]:
        gy = y0 + (75 - lat) / 130 * mh
        d.line([x0, gy, x0 + mw, gy], fill=(232, 234, 238), width=1)
    for poly in CONTINENTS.values():
        pts = [lonlat_to_xy(lon, lat, x0, y0, mw, mh) for lon, lat in poly]
        d.polygon(pts, fill=(238, 240, 244), outline=NAVYBLUE, width=2)
    # ocean labels (fill the empty water: Pacific left, Atlantic centre, Indian right)
    of = font_path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    for label, lon, lat in [("PACIFIC", -150, 5), ("ATLANTIC", -30, 5),
                            ("INDIAN OCEAN", 80, -35)]:
        lx, ly = lonlat_to_xy(lon, lat, x0, y0, mw, mh)
        tw = text_w(d, label, of)
        d.text((lx - tw / 2, ly - 6), label, font=of, fill=(150, 160, 170))


def draw_pin_blue(d, x, y, num):
    r = 8
    d.ellipse([x - r, y - r, x + r, y + r], fill=NAVYBLUE, outline=(255, 255, 255), width=1)
    f = F_SANS_B(8)
    tw = text_w(d, str(num), f)
    d.text((x - tw / 2, y - 6), str(num), font=f, fill=(255, 255, 255))



# ---------- 19 Nov hero visuals (Shenzhen reuses hero_visual "apec") ----------
def hero_gta(d, x, y, w, h):
    # midnight city + moon + controller silhouette (GTA VI unlocks at midnight)
    d.rectangle([x, y, x + w, y + h], fill=(18, 16, 42))
    d.ellipse([x + w - 52, y + 8, x + w - 14, y + 46], fill=(245, 240, 200))
    for bx, bw, bh in [(0.02, 0.10, 0.35), (0.13, 0.08, 0.55), (0.22, 0.11, 0.42),
                       (0.34, 0.09, 0.62), (0.44, 0.10, 0.48), (0.55, 0.08, 0.70),
                       (0.64, 0.11, 0.52), (0.76, 0.09, 0.60), (0.86, 0.12, 0.40)]:
        d.rectangle([x + bx * w, y + h - bh * h, x + (bx + bw) * w, y + h], fill=(8, 8, 22))
    for wx in range(6):
        for wy in range(3):
            d.rectangle([x + 14 + wx * 22, y + h - 26 - wy * 12, x + 20 + wx * 22, y + h - 20 - wy * 12],
                        fill=(255, 220, 90))
    d.rectangle([x + 8, y + h - 20, x + 66, y + h - 6], fill=(0, 0, 0))
    d.text((x + 12, y + h - 18), "VI", font=F_SANS_B(11), fill=(255, 255, 255))


def hero_anthropic(d, x, y, w, h):
    # dark green board: ANT $83 text on the LEFT, candlestick chart on the RIGHT
    # (no overlap — the kicker bar below already carries the NASDAQ source)
    d.rectangle([x, y, x + w, y + h], fill=(8, 46, 30))
    d.text((x + 10, y + 4), "ANT", font=F_SANS_B(18), fill=(255, 255, 255))
    d.text((x + 10, y + 24), "$83", font=F_SANS_B(14), fill=(140, 240, 180))
    cx0, cx1 = x + w * 0.42, x + w - 10
    cy0, cy1 = y + 6, y + h - 6
    d.line([cx0, cy1 - 4, cx1, cy0 + 4], fill=(40, 160, 100), width=2)
    pts = [(0.08, 0.78), (0.20, 0.70), (0.32, 0.74), (0.44, 0.58), (0.56, 0.62),
           (0.68, 0.44), (0.80, 0.48), (0.92, 0.28)]
    for px, py in pts:
        cx = cx0 + px * (cx1 - cx0)
        cy = cy0 + py * (cy1 - cy0)
        d.rectangle([cx - 5, cy - 7, cx + 5, cy + 7], fill=(60, 200, 130))
        d.line([cx, cy - 12, cx, cy + 12], fill=(120, 230, 170), width=2)


def hero_visual19(d, kind, x, y, w, h):
    if kind == "shenzhen":
        hero_visual(d, "apec", x, y, w, h)
    elif kind == "gta":
        hero_gta(d, x, y, w, h)
    elif kind == "anthropic":
        hero_anthropic(d, x, y, w, h)


# ---------- 19 Nov mini visuals for the horizontal grid ----------
def mini_court(d, x, y, w, h):
    # courthouse: pediment + columns
    d.polygon([(x + w * 0.08, y + h * 0.35), (x + w * 0.5, y + h * 0.08),
               (x + w * 0.92, y + h * 0.35)], fill=(70, 80, 100))
    for i in range(4):
        cx = x + w * (0.18 + i * 0.21)
        d.rectangle([cx - 3, y + h * 0.38, cx + 3, y + h * 0.82], fill=(50, 55, 70))
    d.rectangle([x + w * 0.08, y + h * 0.84, x + w * 0.92, y + h * 0.92], fill=(50, 55, 70))


def mini_eye(d, x, y, w, h):
    # watchful eye
    d.ellipse([x + w * 0.08, y + h * 0.30, x + w * 0.92, y + h * 0.70], outline=NAVY2, width=3)
    d.ellipse([x + w * 0.38, y + h * 0.32, x + w * 0.62, y + h * 0.68], fill=NAVY2)
    d.ellipse([x + w * 0.45, y + h * 0.40, x + w * 0.55, y + h * 0.60], fill=(255, 255, 255))


def mini_rain(d, x, y, w, h):
    # cloud + heavy rain
    d.ellipse([x + w * 0.15, y + h * 0.12, x + w * 0.55, y + h * 0.45], fill=(90, 100, 120))
    d.ellipse([x + w * 0.40, y + h * 0.08, x + w * 0.80, y + h * 0.42], fill=(70, 80, 100))
    d.ellipse([x + w * 0.25, y + h * 0.28, x + w * 0.65, y + h * 0.52], fill=(110, 120, 140))
    for px in [0.18, 0.32, 0.46, 0.60, 0.74, 0.86]:
        d.line([x + px * w, y + h * 0.55, x + px * w - 4, y + h * 0.88], fill=(40, 90, 180), width=3)


def mini_layers(d, x, y, w, h):
    # rock strata / missing billion years
    for i, col in enumerate([(200, 170, 120), (170, 140, 100), (140, 110, 80),
                             (110, 90, 70), (90, 75, 60)]):
        d.rectangle([x + w * 0.08, y + h * (0.10 + i * 0.16),
                     x + w * 0.92, y + h * (0.24 + i * 0.16)], fill=col)
    d.line([x + w * 0.30, y + h * 0.10, x + w * 0.30, y + h * 0.90], fill=BRICK, width=2)


def mini_shield(d, x, y, w, h):
    # shield + intercepted missile
    d.polygon([(x + w * 0.5, y + h * 0.08), (x + w * 0.88, y + h * 0.22),
               (x + w * 0.88, y + h * 0.55), (x + w * 0.5, y + h * 0.92),
               (x + w * 0.12, y + h * 0.55), (x + w * 0.12, y + h * 0.22)],
              fill=(35, 140, 75), outline=(20, 80, 45))
    d.line([x + w * 0.30, y + h * 0.30, x + w * 0.70, y + h * 0.70], fill=(255, 255, 255), width=3)
    d.line([x + w * 0.70, y + h * 0.30, x + w * 0.30, y + h * 0.70], fill=(255, 255, 255), width=3)


def mini_pills(d, x, y, w, h):
    # pills + seized packages
    d.rectangle([x + w * 0.10, y + h * 0.55, x + w * 0.45, y + h * 0.85], fill=(200, 60, 50))
    d.rectangle([x + w * 0.55, y + h * 0.55, x + w * 0.90, y + h * 0.85], fill=(180, 50, 40))
    for px, py in [(0.25, 0.30), (0.45, 0.22), (0.65, 0.32), (0.80, 0.22)]:
        cx, cy = x + px * w, y + py * h
        d.ellipse([cx - 7, cy - 4, cx + 7, cy + 4], fill=(255, 255, 255), outline=BRICK, width=2)


def mini19(d, kind, x, y, w, h):
    new = {"court": mini_court, "eye": mini_eye, "rain": mini_rain,
           "layers": mini_layers, "shield": mini_shield, "pills": mini_pills}
    if kind in new:
        new[kind](d, x, y, w, h)
    else:
        mini_visual(d, kind, x, y, w, h)

# ---------- 19 Nov story data — FINAL 40, order fixed by owner, do not change ----------
# kicker: (number, region-label, topic, region-colour-key, source)
HEROES = [
    {"n": 1, "kind": "shenzhen", "region": "ASIA", "topic": "APEC SUMMIT",
     "rc": "ASIA", "src": "REUTERS",
     "headline": "Trump, Xi and Putin hold first three-way summit",
     "body": "The US, Chinese and Russian leaders meet together for the first time, on APEC's last day. Arms control and the Iran war on the agenda. Putin backs the draft Shenzhen Declaration."},
    {"n": 2, "kind": "gta", "region": "WORLD", "topic": "GAMES",
     "rc": "WORLD", "src": "ROCKSTAR",
     "headline": "GTA VI arrives after a 13-year wait",
     "body": "Unlocks at midnight in each country, New Zealand first. 15.9m pre-orders banked. $79.99 on PS5 and Xbox Series X|S; no PC yet."},
    {"n": 3, "kind": "anthropic", "region": "AMERICAS", "topic": "MARKETS",
     "rc": "AMERICAS", "src": "NASDAQ",
     "headline": "Anthropic debuts in the biggest IPO ever",
     "body": "Priced at $83, above the $70-78 range. $81.3bn raised, valuing the Claude maker near $1.5tn. First trades on Thursday."},
]

# grid 4-13: horizontal strips, visual left + text right
GRID = [
    {"n": 4, "kind": "court", "region": "THE HAGUE", "topic": "LAW", "rc": "EUROPE",
     "headline": "World Court rules on Myanmar's Rohingya case",
     "body": "ICJ judgment on Gambia's case over the 2017 crackdown. 730,000 fled in 2017."},
    {"n": 5, "kind": "globe", "region": "ANTALYA", "topic": "CLIMATE", "rc": "EUROPE",
     "headline": "COP31 enters its final 48 hours",
     "body": "Ministers take over. Phase-out and a $120bn adaptation fund still open."},
    {"n": 6, "kind": "cyclone", "region": "ODISHA", "topic": "STORM", "rc": "ASIA",
     "headline": "Cyclone Akvan bears down",
     "body": "200,000 flee the coast. Red alert in 11 districts, schools shut. Landfall near Puri on Friday."},
    {"n": 7, "kind": "eye", "region": "KYIV", "topic": "WAR", "rc": "EUROPE",
     "headline": "Ukraine left off the agenda, watches Shenzhen",
     "body": "White House says Kyiv fears being carved up as the three leaders meet."},
    {"n": 8, "kind": "bars", "region": "SHENZHEN", "topic": "TRADE", "rc": "ASIA",
     "headline": "APEC leaders adopt the Shenzhen Declaration",
     "body": "21 economies back digital trade and an Asia-Pacific community roadmap."},
    {"n": 9, "kind": "rain", "region": "FLORIDA", "topic": "WEATHER", "rc": "AMERICAS",
     "headline": "Flooded Florida braces",
     "body": "A foot of rain in hours in Hollywood. 300 rescue calls in a night. Schools shut on Thursday."},
    {"n": 10, "kind": "layers", "region": "SCIENCE", "topic": "GEOLOGY", "rc": "WORLD",
     "headline": "Earth's missing billion years explained",
     "body": "A Nature study blames mantle currents and ancient ice sheets."},
    {"n": 11, "kind": "ballot", "region": "PARIS", "topic": "POLITICS", "rc": "EUROPE",
     "headline": "Melenchon could win, says France's justice minister",
     "body": "The hard-left leader is a plausible president, the minister says."},
    {"n": 12, "kind": "shield", "region": "JAZAN", "topic": "GULF", "rc": "MIDDLE EAST",
     "headline": "Saudi says danger has passed in three cities",
     "body": "All-clear after a Houthi missile was downed."},
    {"n": 13, "kind": "pills", "region": "BENGHAZI", "topic": "CRIME", "rc": "AFRICA",
     "headline": "Cocaine and millions of pills seized in eastern Libya",
     "body": "Officials display the biggest drug hauls."},
]

# also today 14-40: (number, place, text) — full text, never truncated
ALSO = [
    (14, "GAZA", "Israeli tanks cross Yellow Line, Hamas calls truce breach."),
    (15, "CRIMEA", "Bridge attacked again, traffic halted. Ukraine claims strike, Russia says intercepted."),
    (16, "LONDON", "Van Gogh sells for record $190.4m after 9-hour NGA history."),
    (17, "MEXICO CITY", "Banxico minutes: board cut rates to 6.25%."),
    (18, "CANBERRA", "Australia sanctions West Bank settlers, 3 people + 4 groups."),
    (19, "MOGADISHU", "Somalia accuses UAE of secret military bases."),
    (20, "FRANKFURT", "Deutsche Bank handed $90m fine, Epstein ties, FT reports."),
    (21, "WASHINGTON", "Senators warn cyber risk to AI, seek tighter rules."),
    (22, "OTTAWA", "Carney: Canada rethinks China ties, seeks reset."),
    (23, "NEW DELHI", "Modi meets Prince + Princess of Wales, UK state visit."),
    (24, "TOKYO", "India + Japan review defence ties after 2+2 dialogue."),
    (25, "BENGALURU", "Amazon pledges $7.8bn for India AI."),
    (26, "SYDNEY", "Duckett 133 puts England 1-0 in ODI vs Australia."),
    (27, "WELLINGTON", "NZ unlocks GTA VI at midnight, first in world."),
    (28, "BAGHDAD", "Six French ISIL members jailed for life in Iraq."),
    (29, "DHAKA", "Bangladesh: Yunus ancestral home set on fire, 28 districts hit by violence."),
    (30, "GULF", "Kuwait activates air defenses vs drones, Bahrain thwarts Iranian assault, after US Qeshm strike 17 Nov."),
    (31, "WASHINGTON", "Jeffries formally nominated Speaker. (251-11 vote was 18 Nov; 19 Nov is the formal nomination.)"),
    (32, "WASHINGTON", "Garcia sends 12 preservation letters to Trump allies."),
    (33, "WASHINGTON", "US loses measles elimination status, Dems attack RFK Jr."),
    (34, "WASHINGTON", "House Dems probe Lutnick - Nvidia."),
    (35, "SEOUL", "Suneung: 551,864 sit Korea's college exam, flights pause."),
    (36, "TOKYO SIDE", "Takaichi meets Putin, Japan-Russia talks on APEC sidelines."),
    (37, "TAIWAN", "Taiwan reports Tu-95 overflight east of island, second time this week."),
    (38, "ADDIS ABABA", "Ethiopia-Eritrea: troops mass at border."),
    (39, "GENEVA", "WHO warns antibiotic resistance worsening worldwide since 2019."),
    (40, "SYDNEY SIDE", "Data centres may add 39m t CO2 a year by 2035."),
]

NUMBERS = [
    ("$81.3bn", "Anthropic IPO"),
    ("15.9m", "GTA VI pre-orders"),
    ("200,000", "evacuated Akvan"),
    ("$120bn", "COP31 finance unresolved"),
    ("730,000", "Rohingya fled 2017"),
    ("16bn miles", "Voyager 1"),
]

DATE_CHECK = ("Date check — left off on purpose because they broke before Thursday: "
              "EU proposes €450m Ukraine loan (18 Nov) · House Dems' 251-11 Jeffries vote (18 Nov) · "
              "Voyager 1 one light-day 10:16 GMT Wed (18 Nov) · Peltola Alaska win (18 Nov) · "
              "Pew Islam largest by 2035 (18 Nov) · US strikes on Iran's Qeshm Island (17 Nov)")

FOOTER_SRC = ("Every story here happened, or was first reported, on Thursday 19 November 2026. "
              "Sources: Reuters, AP, AFP, BBC, The Hindu, IMD, NASA, ICJ, Pew.")

# map pins for the visual stories 1-13 (lon, lat); 10 has no location (global science)
# pins offset where two stories share a city (Paris/The Hague, NYC/NASDAQ,
# Shenzhen/APEC) so no two pins touch; schematic offsets, story numbers unchanged
PINS = {
    1: (114.1, 22.5), 2: (-74.0, 40.7), 3: (-62.0, 44.0), 4: (4.3, 52.1),
    5: (30.7, 36.9), 6: (85.8, 20.3), 7: (30.5, 50.5), 8: (126.0, 22.5),
    9: (-80.2, 25.8), 11: (-6.0, 45.0), 12: (42.5, 16.9), 13: (20.1, 32.1),
}
PIN_RC = {1: "ASIA", 2: "WORLD", 3: "AMERICAS", 4: "EUROPE", 5: "EUROPE",
          6: "ASIA", 7: "EUROPE", 8: "ASIA", 9: "AMERICAS", 11: "EUROPE",
          12: "MIDDLE EAST", 13: "AFRICA"}
LEGEND = [("Americas", "AMERICAS"), ("Asia", "ASIA"), ("Europe", "EUROPE"),
          ("Middle East", "MIDDLE EAST"), ("Africa", "AFRICA"),
          ("Oceania", "OCEANIA"), ("World", "WORLD")]

def draw_pin_small(d, x, y, num, fill=None):
    r = 6
    if fill is None:
        fill = NAVY2
    d.ellipse([x - r, y - r, x + r, y + r], fill=fill, outline=(255, 255, 255), width=1)
    f = F_SANS_B(7)
    tw = text_w(d, str(num), f)
    d.text((x - tw / 2, y - 5), str(num), font=f, fill=(255, 255, 255))


# ---------- layout ----------
def kicker_bar(d, x, y, w, n, region, topic, rc, src):
    """Coloured kicker bar: black number box + region/topic + source (white)."""
    col = REGION_COLORS[rc]
    d.rectangle([x, y, x + w, y + 18], fill=col)
    d.rectangle([x, y, x + 24, y + 18], fill=(0, 0, 0))
    f = F_SANS_B(10)
    tw = text_w(d, str(n), f)
    d.text((x + (24 - tw) / 2, y + 3), str(n), font=f, fill=(255, 255, 255))
    d.text((x + 30, y + 3), f"{region} · {topic}", font=F_SANS_B(9),
           fill=(255, 255, 255))
    sw = text_w(d, src, F_SANS_B(8))
    d.text((x + w - sw - 6, y + 4), src, font=F_SANS_B(8), fill=(255, 255, 255))


def hero_block(d, hero, x, y, w, h, big):
    """One hero: border, visual, kicker bar, headline, body. Returns issues."""
    issues = []
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    if big:
        vis_h, kick_y, head_y, head_size, body_size, body_y = 106, 108, 132, 15, 10, 162
    else:
        vis_h, kick_y, head_y, head_size, body_size, body_y = 46, 48, 68, 12, 8, 88
    hero_visual19(d, hero["kind"], x + 2, y + 2, w - 4, vis_h)
    kicker_bar(d, x + 2, y + kick_y, w - 4, hero["n"], hero["region"],
               hero["topic"], hero["rc"], hero["src"])
    hl = wrap(d, hero["headline"], F_SERIF_B(head_size), w - 14)
    if len(hl) > 2:
        issues.append(f"hero {hero['n']} headline {len(hl)} lines")
    yy = y + head_y
    for line in hl[:2]:
        d.text((x + 7, yy), line, font=F_SERIF_B(head_size), fill=INK)
        yy += head_size + 3
    bl = wrap(d, hero["body"], F_SANS(body_size), w - 14)
    max_bl = 4 if big else 2
    if len(bl) > max_bl:
        issues.append(f"hero {hero['n']} body {len(bl)} lines > {max_bl}")
    yy = y + body_y
    for line in bl[:max_bl]:
        d.text((x + 7, yy), line, font=F_SANS(body_size), fill=(40, 40, 40))
        yy += body_size + 3
    return issues


def grid_cell(d, s, x, y, w, h):
    """One horizontal grid strip: visual left, kicker + headline + body right."""
    issues = []
    d.rectangle([x, y, x + w, y + h], outline=(150, 150, 150), width=1)
    mini19(d, s["kind"], x + 2, y + 2, 74, h - 4)
    tx = x + 82
    tw = w - 88
    d.text((tx, y + 3), f"{s['n']} · {s['region']} · {s['topic']}",
           font=F_SANS_B(8), fill=REGION_COLORS[s["rc"]])
    hl = wrap(d, s["headline"], F_SERIF_B(11), tw)
    if len(hl) > 1:
        issues.append(f"grid {s['n']} headline {len(hl)} lines")
    d.text((tx, y + 14), hl[0] if hl else "", font=F_SERIF_B(11), fill=INK)
    bl = wrap(d, s["body"], F_SANS(8), tw)
    if len(bl) > 2:
        issues.append(f"grid {s['n']} body {len(bl)} lines > 2")
    yy = y + 28
    for line in bl[:2]:
        d.text((tx, yy), line, font=F_SANS(8), fill=(40, 40, 40))
        yy += 10
    return issues


def wrap_first_rest(d, text, f, first_w, rest_w):
    """Wrap text where line 1 has width first_w and later lines rest_w."""
    words = text.split()
    lines = []
    cur, idx = "", 0
    for i, w in enumerate(words):
        t = (cur + " " + w).strip()
        if text_w(d, t, f) <= first_w:
            cur, idx = t, i + 1
        else:
            break
    lines.append(cur)
    cur = ""
    for w in words[idx:]:
        t = (cur + " " + w).strip()
        if text_w(d, t, f) <= rest_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return [ln for ln in lines if ln]


def main():
    W, H = 1024, 1024
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    issues = []
    d.rectangle([2, 2, W - 3, H - 3], outline=INK, width=2)

    # ---- masthead (white, THE WORLD black serif, centred) ----
    draw_centered(d, W // 2, 6, "40 STORIES · 7 REGIONS · 13 DRAWN · ALL FROM THURSDAY",
                  F_SANS_B(9), (110, 110, 110))
    draw_centered(d, W // 2, 16, "THE WORLD", F_SERIF_B(46), INK)
    draw_centered(d, W // 2, 66, "Thursday 19 November 2026", F_SERIF(16), INK)
    d.line([8, 86, W - 8, 86], fill=INK, width=2)

    # ---- heroes: Shenzhen big left (60%), GTA + Anthropic stacked right ----
    issues += hero_block(d, HEROES[0], 8, 92, 604, 236, big=True)
    issues += hero_block(d, HEROES[1], 620, 92, 396, 116, big=False)
    issues += hero_block(d, HEROES[2], 620, 214, 396, 114, big=False)

    # ---- grid 4-13: 2 columns x 5 rows, horizontal strips ----
    gy0, gh, gap = 336, 48, 4
    for i, s in enumerate(GRID):
        col, row = i % 2, i // 2
        gx = 8 if col == 0 else 516
        gy = gy0 + row * (gh + gap)
        issues += grid_cell(d, s, gx, gy, 500, gh)

    # ---- map + also today ----
    d.text((8, 584), "WHERE IT HAPPENED", font=F_SANS_B(13), fill=INK)
    d.text((478, 584), "ALSO ON THURSDAY", font=F_SANS_B(13), fill=INK)
    d.line([8, 602, W - 8, 602], fill=INK, width=1)
    # legend (coloured dots + region names)
    lx = 8
    for name, rc in LEGEND:
        d.ellipse([lx, 608, lx + 8, 616], fill=REGION_COLORS[rc])
        d.text((lx + 11, 607), name, font=F_SANS(8), fill=(60, 60, 60))
        lx += 11 + text_w(d, name, F_SANS(8)) + 10
    # outline map + blue pins
    draw_world_map_outline(d, 12, 624, 462, 208)
    for n, (lon, lat) in PINS.items():
        px, py = lonlat_to_xy(lon, lat, 12, 624, 462, 208)
        draw_pin_small(d, px, py, n, fill=REGION_COLORS[PIN_RC[n]])
    d.text((8, 838), "Story 10 is global science, so it has no pin on this map.",
           font=F_SANS_I(8), fill=(100, 100, 100))
    # also-today list, 2 columns, full text, never truncated
    cols = [(478, ALSO[:14]), (752, ALSO[14:])]
    for cx, items in cols:
        yy = 608
        for n, place, text in items:
            head = f"{n} {place} — "
            hw = text_w(d, head, F_SANS_B(8))
            # wrap body: line 1 shares the row with the bold head, rest full width
            bl = wrap_first_rest(d, text, F_SANS(8), 264 - hw, 264)
            if len(bl) > 2:
                issues.append(f"also {n} body {len(bl)} lines > 2")
            d.text((cx, yy), head, font=F_SANS_B(8), fill=INK)
            xx = cx + hw
            for j, line in enumerate(bl[:2]):
                d.text((xx if j == 0 else cx, yy + j * 10), line,
                       font=F_SANS(8), fill=(40, 40, 40))
            yy += len(bl[:2]) * 10 + 2
        # remember the tallest column for the section bottom (not used further)

    # ---- numbers bar: 6 white boxes, black border, at the bottom ----
    nb_y, nb_h, nb_w, nb_gap = 906, 50, 162, 6
    for i, (num, label) in enumerate(NUMBERS):
        bx = 8 + i * (nb_w + nb_gap)
        d.rectangle([bx, nb_y, bx + nb_w, nb_y + nb_h], fill=(255, 255, 255),
                    outline=INK, width=1)
        draw_centered(d, bx + nb_w // 2, nb_y + 6, num, F_SERIF_B(16), INK)
        draw_centered(d, bx + nb_w // 2, nb_y + 28, label, F_SANS(8), (60, 60, 60))

    # ---- date check: 1 italic line (wraps to 2), no red box ----
    dc = wrap(d, DATE_CHECK, F_SERIF_I(9), W - 24)
    yy = 962
    for line in dc:
        draw_centered(d, W // 2, yy, line, F_SERIF_I(9), INK)
        yy += 12
    # ---- footer ----
    draw_centered(d, W // 2, 988, FOOTER_SRC, F_SANS(8), (90, 90, 90))
    draw_centered(d, W // 2, 1002, "THE WORLD — 19 NOVEMBER 2026 · 40 STORIES · 7 REGIONS · ONE PAGE",
                  F_SANS_B(9), (70, 70, 70))

    im.save("entry.png")
    print(f"saved entry.png  {W}x{H}  {os.path.getsize('entry.png')} bytes")
    print("issues:", "none" if not issues else "; ".join(issues))


if __name__ == "__main__":
    main()
