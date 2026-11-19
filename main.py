"""news-image-20261119 V2 — entry program (Python 3.13, standard library only).

The entry is the image entry.png beside this file (a 1024x1024 PNG front page
summing up 19 November 2026 world news, drawn beforehand with Pillow).
V2 follows the Rank #2 LOOK (owner order): warm cream paper, numbers bar on
TOP, 3 heroes across, box grid, navy dot-matrix map + red pins, Date Check
red box. ALL sentences are REWRITTEN (different words from V1 and from Rank
#2, same 40 stories/themes), with 40 stories all from Thursday 19 November
2026: Shenzhen summit, GTA VI, Anthropic IPO, ICJ Rohingya judgment, COP31,
Cyclone Akvan and 34 more.
Palette: cream paper + black + dark red + navy. Serif headlines, sans body.
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
