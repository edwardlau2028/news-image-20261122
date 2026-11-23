[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/edwardlau2028/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/edwardlau2028/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# The World in One Day — 22 November 2026

A newspaper-style front page summing up Sunday 22 November 2026's world
news in one 1024×1024 image, built for the make.fun competition
[news-image-20261122](https://make.fun/bounty/news-image-20261122).
Every story below happened, or was first reported, on 22 November 2026.

## The eight stories

1. **CLIMATE — COP31 talks collapse, no deal.** EU rejects a pact that
   omits fossil fuels; longest COP ever.
2. **UKRAINE — Drone flattens flats near Kyiv.** At least 4 killed in
   Dymer; a boy survives 14 hours in rubble.
3. **USA — Democrats clinch 258 House seats.** Largest House majority
   since 1992, after a North Carolina win.
4. **USA — Trump orders contractors to alert White House.** Firms must
   flag Congress's oversight requests to the White House.
5. **USA — Trump backs a 10% credit card cap.** President says he will
   work with Democrats on the rate cap.
6. **WEST BANK — Eisenkot condemns settler arson.** Settlers torch West
   Bank villages; police investigate.
7. **SPORT — Alcaraz wins maiden ATP Finals.** Beats world No. 1 Zverev
   6-2, 7-6 to take the title.
8. **TECH — US probes Nvidia's chip sales to China.** Bessent seeks
   answers on who ran compliance at Nvidia.

Sources: Reuters · AP · AFP · Al Jazeera.

## How it runs

`draw_news.py` draws the front page with Python and Pillow, using the
Noto fonts, and writes `entry.png` (1024×1024, under 1 MiB). `main.ts`
(Node 22, standard library only) copies that image to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`).

```sh
python3 draw_news.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Repository

https://github.com/edwardlau2028/news-image-20261122

## License

MIT — see [LICENSE](LICENSE).
