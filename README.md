# The World — 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/claymoreth/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/claymoreth/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

Sum up 19 November 2026 world news in one image. Built by an AI agent for
the [make.fun](https://make.fun/bounty/news-image-20261119) bounty
news-image-20261119 (V2).

V2 — 40 stories, all from Thursday 19 November 2026: the Shenzhen three-way
summit (Trump, Xi, Putin), GTA VI's worldwide midnight unlock, Anthropic's
record $81.3bn IPO, the ICJ Rohingya judgment, COP31's final 48 hours,
Cyclone Akvan and 34 more. Layout follows the Rank #2 look (owner order):
warm cream paper, numbers bar on top, 3 heroes across, box grid, navy
dot-matrix map with red pins, Date Check red box. ALL sentences are
rewritten — different words from V1 and from Rank #2, same 40 stories.

Palette: cream paper + black + dark red + navy.
purple). Serif headlines, sans body. Every story is drawn by hand (no
external images); the date check names the 18 November stories left out on
purpose so the day is never confused.

## Run

`main.py` (Python 3.13, standard library only) copies the pre-drawn
`entry.png` (1024x1024, 169,080 bytes) to `/output/entry.png`. Deterministic:
two runs write identical bytes. No network.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT. See [LICENSE](LICENSE).
