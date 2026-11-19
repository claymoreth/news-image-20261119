#!/usr/bin/env python3
"""NEWS-IMAGE-20261119 V2 — Rank #2 LOOK (owner order: bikin seperti ini, dari segi warna apapun, table nya) — cream paper, numbers bar on TOP, 3 heroes across, box grid, navy dot-matrix map + red pins, Date Check red box. ALL sentences REWRITTEN (different words from V1 and from Rank #2, same 40 stories/themes). 40 stories, all Thursday 19 November 2026. Own words — the LOOK follows Rank #2 per owner order, the SENTENCES are all ours.
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
PAPER = (247, 240, 230)          # Rank #2 warm cream paper
BRICK = (178, 60, 40)          # brick red accent
NAVY2 = (20, 50, 90)           # dark blue accent
NAVYBLUE = NAVY2
RED2 = (158, 40, 52)            # Rank #2 dark brick red (numbers, kickers, subtitle)
NAVYMAP = (23, 48, 79)          # Rank #2 dark navy (dot-matrix map)
PINRED = (185, 76, 79)          # Rank #2 red map pins
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


# ---------- Rank #2 dot-matrix map (navy dots) + red pins ----------
def _inside_poly(x, y, poly):
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside


def draw_dotmap(d, x0, y0, mw, mh, step=8, r=2):
    """Navy dot-matrix world map (Rank #2 style): dots inside the continents."""
    for poly in CONTINENTS.values():
        pts = [lonlat_to_xy(lon, lat, x0, y0, mw, mh) for lon, lat in poly]
        minx = min(p[0] for p in pts); maxx = max(p[0] for p in pts)
        miny = min(p[1] for p in pts); maxy = max(p[1] for p in pts)
        gx = minx
        while gx <= maxx:
            gy = miny
            while gy <= maxy:
                if _inside_poly(gx, gy, pts):
                    d.ellipse([gx - r, gy - r, gx + r, gy + r], fill=NAVYMAP)
                gy += step
            gx += step


def draw_pin_red(d, x, y, num):
    r = 7
    d.ellipse([x - r, y - r, x + r, y + r], fill=PINRED, outline=(255, 255, 255), width=1)
    f = F_SANS_B(8)
    tw = text_w(d, str(num), f)
    d.text((x - tw / 2, y - 6), str(num), font=f, fill=(255, 255, 255))


# ---------- V2 story data — SAME 40 stories, ALL sentences REWRITTEN ----------
# (different words from V1 and from Rank #2, same themes/facts)
HEROES = [
    {"n": 1, "kind": "shenzhen", "region": "SHENZHEN", "topic": "SUMMIT",
     "rc": "ASIA", "src": "REUTERS",
     "headline": "Shenzhen hosts a first: three leaders at one table",
     "body": "For the first time, the American, Chinese and Russian presidents sit down together, on APEC's closing day. Arms control and the Iran war top the talks. Putin backs the draft Shenzhen Declaration."},
    {"n": 2, "kind": "gta", "region": "WORLDWIDE", "topic": "GAMES",
     "rc": "WORLD", "src": "ROCKSTAR",
     "headline": "After thirteen years, GTA VI is out at last",
     "body": "The sequel goes live at midnight in every country, with New Zealand first in line. Fans banked 15.9m pre-orders. It costs $79.99 on PS5 and Xbox Series X|S; the PC version is still to come."},
    {"n": 3, "kind": "anthropic", "region": "NEW YORK", "topic": "MARKETS",
     "rc": "AMERICAS", "src": "NASDAQ",
     "headline": "Claude's maker lists in the largest flotation on record",
     "body": "Shares were priced at $83, above the $70-78 range, raising $81.3bn — the biggest IPO ever — and valuing the firm near $1.5tn. Trading begins on Thursday."},
]

GRID = [
    {"n": 4, "kind": "court", "region": "THE HAGUE", "topic": "LAW", "rc": "EUROPE",
     "headline": "The Hague delivers its verdict on Myanmar",
     "body": "The World Court rules on Gambia's case over the 2017 crackdown. The judgment is final. Some 730,000 fled in 2017."},
    {"n": 5, "kind": "globe", "region": "ANTALYA", "topic": "CLIMATE", "rc": "EUROPE",
     "headline": "Climate talks go down to the wire in Antalya",
     "body": "Ministers take over as the summit enters its final two days. A fossil-fuel phase-out and a $120bn adaptation fund are still unresolved."},
    {"n": 6, "kind": "cyclone", "region": "ODISHA", "topic": "STORM", "rc": "ASIA",
     "headline": "A cyclone closes in on Odisha's coast",
     "body": "Some 200,000 people leave the coast. Eleven districts are on red alert and schools are shut. Landfall is expected near Puri on Friday."},
    {"n": 7, "kind": "eye", "region": "KYIV", "topic": "WAR", "rc": "EUROPE",
     "headline": "Kyiv watches the summit from the sidelines",
     "body": "Ukraine is not on the Shenzhen agenda. The White House says Kyiv fears being carved up as the three leaders meet."},
    {"n": 8, "kind": "bars", "region": "SHENZHEN", "topic": "TRADE", "rc": "ASIA",
     "headline": "Twenty-one economies sign up to the Shenzhen plan",
     "body": "APEC's leaders back a declaration on digital trade and a roadmap for an Asia-Pacific community."},
    {"n": 9, "kind": "rain", "region": "FLORIDA", "topic": "WEATHER", "rc": "AMERICAS",
     "headline": "Florida counts the cost of a foot of rain",
     "body": "Hollywood saw a foot of rain in hours. Crews answered 300 rescue calls in a night. Schools stay shut on Thursday."},
    {"n": 10, "kind": "layers", "region": "SCIENCE", "topic": "GEOLOGY", "rc": "WORLD",
     "headline": "A study solves Earth's billion-year gap",
     "body": "A Nature study pins the missing billion years on mantle currents and ancient ice sheets."},
    {"n": 11, "kind": "ballot", "region": "PARIS", "topic": "POLITICS", "rc": "EUROPE",
     "headline": "France's justice minister: Melenchon could win",
     "body": "The hard-left leader is a plausible next president, the minister says."},
    {"n": 12, "kind": "shield", "region": "JAZAN", "topic": "GULF", "rc": "MIDDLE EAST",
     "headline": "Saudi gives the all-clear in three cities",
     "body": "The danger has passed after a Houthi missile was shot down, Riyadh says."},
    {"n": 13, "kind": "pills", "region": "BENGHAZI", "topic": "CRIME", "rc": "AFRICA",
     "headline": "Libya shows off its biggest drug seizures",
     "body": "Officials in eastern Libya display cocaine and millions of pills in the largest hauls yet."},
]

ALSO = [
    (14, "GAZA", "Israeli tanks cross the Yellow Line; Hamas calls it a breach of the truce."),
    (15, "CRIMEA", "The bridge is hit again and traffic stops. Kyiv claims the strike; Moscow says it was intercepted."),
    (16, "LONDON", "A Van Gogh fetches a record $190.4m after nine hours of bidding at the NGA."),
    (17, "MEXICO CITY", "Banxico's minutes show the board cut rates to 6.25%."),
    (18, "CANBERRA", "Australia sanctions three people and four groups over West Bank settlements."),
    (19, "MOGADISHU", "Somalia accuses the UAE of running secret military bases."),
    (20, "FRANKFURT", "Deutsche Bank is fined $90m over Epstein ties, the FT reports."),
    (21, "WASHINGTON", "Senators warn of cyber risk to AI and call for tighter rules."),
    (22, "OTTAWA", "Carney says Canada is rethinking its China ties and wants a reset."),
    (23, "NEW DELHI", "Modi meets the Prince and Princess of Wales on their UK state visit."),
    (24, "TOKYO", "India and Japan review defence ties after their 2+2 dialogue."),
    (25, "BENGALURU", "Amazon pledges $7.8bn for AI in India."),
    (26, "SYDNEY", "Duckett's 133 puts England 1-0 up in the ODI against Australia."),
    (27, "WELLINGTON", "New Zealand is first in the world to unlock GTA VI at midnight."),
    (28, "BAGHDAD", "Six French ISIL members are jailed for life in Iraq."),
    (29, "DHAKA", "Yunus's ancestral home is set on fire as violence hits 28 districts in Bangladesh."),
    (30, "GULF", "Kuwait switches on air defences against drones and Bahrain foils an Iranian assault, days after the US Qeshm strike."),
    (31, "WASHINGTON", "Jeffries is formally nominated as Speaker. (The 251-11 vote was on 18 Nov; the formal nomination is today.)"),
    (32, "WASHINGTON", "Garcia sends 12 preservation letters to Trump allies."),
    (33, "WASHINGTON", "The US loses its measles elimination status; Democrats attack RFK Jr."),
    (34, "WASHINGTON", "House Democrats open a probe into Lutnick and Nvidia."),
    (35, "SEOUL", "Suneung: 551,864 sit South Korea's college exam as flights pause."),
    (36, "TOKYO SIDE", "Takaichi meets Putin for Japan-Russia talks on the APEC sidelines."),
    (37, "TAIWAN", "Taiwan reports a Tu-95 overflight east of the island, the second this week."),
    (38, "ADDIS ABABA", "Ethiopia and Eritrea mass troops at the border."),
    (39, "GENEVA", "The WHO warns antibiotic resistance has worsened worldwide since 2019."),
    (40, "SYDNEY SIDE", "Data centres may add 39m tonnes of CO2 a year by 2035."),
]

NUMBERS = [
    ("$81.3bn", "Anthropic's record IPO"),
    ("13 years", "since GTA V; sequel out today"),
    ("551,864", "sit Korea's college exam"),
    ("200,000", "moved to safety in Odisha"),
    ("$120bn", "COP31 finance goal still open"),
    ("730,000", "Rohingya fled Myanmar in 2017"),
]

SUBTITLE = ("A first three-way summit in Shenzhen · GTA VI goes on sale at midnight · "
            "The biggest IPO ever lists · The World Court rules on Myanmar")

DATE_CHECK = ("DATE CHECK — left off on purpose because they broke before Thursday: "
              "EU proposes €450m Ukraine loan (18 Nov) · House Dems' 251-11 Jeffries vote (18 Nov) · "
              "Voyager 1 one light-day 10:16 GMT Wed (18 Nov) · Peltola Alaska win (18 Nov) · "
              "Pew Islam largest by 2035 (18 Nov) · US strikes on Iran's Qeshm Island (17 Nov)")

FOOTER_SRC = ("Every story here happened, or was first reported, on Thursday 19 November 2026. "
              "Sources: Reuters, AP, AFP, BBC, The Hindu, IMD, NASA, ICJ, Pew.")

PINS = {
    1: (114.1, 22.5), 2: (-74.0, 40.7), 3: (-54.0, 48.0), 4: (4.3, 52.1),
    5: (30.7, 36.9), 6: (85.8, 20.3), 7: (30.5, 50.5), 8: (134.0, 30.0),
    9: (-80.2, 25.8), 11: (-10.0, 42.0), 12: (42.5, 16.9), 13: (16.0, 28.0),
}

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


def hero2(d, hero, x, y, w, h):
    """Rank #2 hero: border, visual on top, RED kicker, serif headline, body."""
    issues = []
    d.rectangle([x, y, x + w, y + h], outline=(120, 120, 120), width=1)
    hero_visual19(d, hero["kind"], x + 1, y + 1, w - 2, 90)
    ky = y + 92
    d.text((x + 6, ky), f"{hero['n']} {hero['region']} · {hero['topic']}",
           font=F_SANS_B(9), fill=RED2)
    sw = text_w(d, hero["src"], F_SANS_B(8))
    d.text((x + w - sw - 6, ky + 1), hero["src"], font=F_SANS_B(8), fill=(110, 110, 110))
    hl = wrap(d, hero["headline"], F_SERIF_B(15), w - 12)
    if len(hl) > 2:
        issues.append(f"hero {hero['n']} headline {len(hl)} lines")
    yy = ky + 16
    for line in hl[:2]:
        d.text((x + 6, yy), line, font=F_SERIF_B(15), fill=INK)
        yy += 18
    bl = wrap(d, hero["body"], F_SANS(9), w - 12)
    if len(bl) > 3:
        issues.append(f"hero {hero['n']} body {len(bl)} lines > 3")
    for line in bl[:3]:
        d.text((x + 6, yy), line, font=F_SANS(9), fill=(40, 40, 40))
        yy += 12
    return issues


def grid2(d, s, x, y, w, h):
    """Rank #2 grid box: border, visual on top, RED kicker, serif headline, body."""
    issues = []
    d.rectangle([x, y, x + w, y + h], outline=(150, 150, 150), width=1)
    mini19(d, s["kind"], x + 1, y + 1, w - 2, 40)
    ky = y + 42
    d.text((x + 5, ky), f"{s['n']} · {s['region']} · {s['topic']}",
           font=F_SANS_B(8), fill=RED2)
    hl = wrap(d, s["headline"], F_SERIF_B(11), w - 10)
    if len(hl) > 2:
        issues.append(f"grid {s['n']} headline {len(hl)} lines")
    yy = ky + 12
    for line in hl[:2]:
        d.text((x + 5, yy), line, font=F_SERIF_B(11), fill=INK)
        yy += 14
    bl = wrap(d, s["body"], F_SANS(8), w - 10)
    if len(bl) > 3:
        issues.append(f"grid {s['n']} body {len(bl)} lines > 3")
    for line in bl[:3]:
        d.text((x + 5, yy), line, font=F_SANS(8), fill=(40, 40, 40))
        yy += 10
    return issues


def main():
    W, H = 1024, 1024
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    issues = []
    d.rectangle([2, 2, W - 3, H - 3], outline=INK, width=2)

    # ---- tagline row (Rank #2: red left, grey right) ----
    d.text((8, 8), "THE WORLD IN ONE PICTURE", font=F_SANS_B(10), fill=RED2)
    rt = "40 STORIES · EVERY ONE FROM THURSDAY 19 NOVEMBER"
    d.text((W - 8 - text_w(d, rt, F_SANS_B(9)), 9), rt, font=F_SANS_B(9),
           fill=(110, 110, 110))
    # ---- title (large black serif, left) ----
    d.text((8, 22), "Thursday 19 November 2026", font=F_SERIF_B(40), fill=INK)
    # ---- subtitle (red line) ----
    d.text((8, 66), SUBTITLE, font=F_SERIF_I(12), fill=RED2)
    d.line([8, 86, W - 8, 86], fill=INK, width=1)

    # ---- numbers bar on TOP (Rank #2: red numbers, grey labels) ----
    nb_y, nb_h = 92, 38
    col_w = (W - 16) / 6.0
    for i, (num, label) in enumerate(NUMBERS):
        cx = 8 + col_w * i + col_w / 2
        draw_centered(d, cx, nb_y, num, F_SERIF_B(18), RED2)
        ll = wrap(d, label, F_SANS(8), col_w - 12)
        yy = nb_y + 22
        for line in ll[:2]:
            draw_centered(d, cx, yy, line, F_SANS(8), (90, 90, 90))
            yy += 10
        if i > 0:
            d.line([8 + col_w * i, nb_y + 2, 8 + col_w * i, nb_y + nb_h - 2],
                   fill=(180, 180, 180), width=1)
    d.line([8, nb_y + nb_h + 4, W - 8, nb_y + nb_h + 4], fill=INK, width=1)

    # ---- heroes: 3 across ----
    hy, hh = 140, 190
    hw = (W - 16 - 2 * 8) / 3.0
    for i, hero in enumerate(HEROES):
        hx = 8 + i * (hw + 8)
        issues += hero2(d, hero, hx, hy, hw, hh)

    # ---- grid: 5 columns x 2 rows = stories 4-13 ----
    gy0, gh, gap = 338, 118, 6
    gw = (W - 16 - 4 * gap) / 5.0
    for i, s in enumerate(GRID):
        col, row = i % 5, i // 5
        gx = 8 + col * (gw + gap)
        gy = gy0 + row * (gh + gap)
        issues += grid2(d, s, gx, gy, gw, gh)

    # ---- map + also today ----
    d.text((8, 584), "WHERE IT HAPPENED", font=F_SANS_B(13), fill=INK)
    d.text((408, 584), "ALSO ON THURSDAY 19 NOVEMBER", font=F_SANS_B(13), fill=INK)
    d.line([8, 602, W - 8, 602], fill=INK, width=1)
    # navy dot-matrix map + red pins
    draw_dotmap(d, 12, 608, 380, 210)
    for n, (lon, lat) in PINS.items():
        px, py = lonlat_to_xy(lon, lat, 12, 608, 380, 210)
        draw_pin_red(d, px, py, n)
    d.text((8, 824), "Red = stories 1-13. Story 10 is global science, so it has no pin.",
           font=F_SANS_I(8), fill=(100, 100, 100))
    # also-today list, 2 columns, full text, never truncated
    cols = [(408, ALSO[:14]), (712, ALSO[14:])]
    for cx, items in cols:
        yy = 608
        for n, place, text in items:
            head = f"{n} {place} — "
            hw2 = text_w(d, head, F_SANS_B(8))
            bl = wrap_first_rest(d, text, F_SANS(8), 296 - hw2, 296)
            if len(bl) > 2:
                issues.append(f"also {n} body {len(bl)} lines > 2")
            d.text((cx, yy), head, font=F_SANS_B(8), fill=INK)
            xx = cx + hw2
            for j, line in enumerate(bl[:2]):
                d.text((xx if j == 0 else cx, yy + j * 9), line,
                       font=F_SANS(8), fill=(40, 40, 40))
            yy += len(bl[:2]) * 9 + 1

    # ---- date check: RED box (Rank #2) ----
    dc_y, dc_h = 890, 44
    d.rectangle([8, dc_y, W - 8, dc_y + dc_h], outline=RED2, width=2)
    dc = wrap(d, DATE_CHECK, F_SANS(9), W - 40)
    yy = dc_y + 5
    for line in dc[:2]:
        d.text((16, yy), line, font=F_SANS(9), fill=INK)
        yy += 12
    if len(dc) > 2:
        issues.append(f"date check {len(dc)} lines > 2")

    # ---- footer ----
    draw_centered(d, W // 2, 942, FOOTER_SRC, F_SANS(8), (90, 90, 90))
    draw_centered(d, W // 2, 956, "THE WORLD — 19 NOVEMBER 2026 · 40 STORIES · 7 REGIONS · ONE PAGE",
                  F_SANS_B(9), (70, 70, 70))

    im.save("entry.png")
    print(f"saved entry.png  {W}x{H}  {os.path.getsize('entry.png')} bytes")
    print("issues:", "none" if not issues else "; ".join(issues))


if __name__ == "__main__":
    main()
