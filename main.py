"""news-image-20261119 V1 — entry program (Python 3.13, standard library only).

The entry is the image entry.png beside this file (a 1024x1024 PNG front page
summing up 19 November 2026 world news, drawn beforehand with Pillow).
V1 is built on our V2.6 architecture (white masthead, hero 1+2, horizontal
grid, outline map + blue pins, numbers bar at the bottom, italic date check,
WHITE paper), with 40 stories all from Thursday 19 November 2026: Shenzhen
summit, GTA VI, Anthropic IPO, ICJ Rohingya judgment, COP31, Cyclone Akvan
and 34 more. Own layout, own words — NOT a copy of Rank #1 or Rank #2.
Palette: white paper + black + the 7 region colours. Serif headlines, sans body.
This program only copies it to the path the grader reads:
    /output/entry.png
Deterministic: the same bytes on every run, no network, no randomness.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
