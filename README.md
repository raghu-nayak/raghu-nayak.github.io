# raghu-nayak.github.io

The landing page at **[raghu-nayak.github.io](https://raghu-nayak.github.io/)** — one
self-contained HTML file that lists the calculators, built from the same design tokens
they use so the three pages read as one thing.

No build step, no dependencies, no network requests: the card previews are real
screenshots of each tool, inlined as WebP data URIs, in both light and dark.

## What it links to

| Calculator | Live | Source |
| --- | --- | --- |
| **Australian FIRE Calculator** — the earliest you could stop working, with super and everything outside it modelled apart | [open](https://raghu-nayak.github.io/au-fire-calculator/) | [repo](https://github.com/raghu-nayak/au-fire-calculator) |
| **Investment Growth Calculator** — what contributions, returns, fees, tax and inflation do to a portfolio | [open](https://raghu-nayak.github.io/investment-calc/) | [repo](https://github.com/raghu-nayak/investment-calc) |

## Run it locally

```sh
open index.html          # macOS
xdg-open index.html      # Linux
start index.html         # Windows
```

`file://` behaves exactly like `https://` — there is nothing to serve.

## Regenerating the previews

The screenshots go stale when either calculator changes. Rebuild all four:

```sh
python3 tools/shots.py
```

Needs Google Chrome and `cwebp` (`brew install webp`). It expects the calculators
checked out beside this repo:

```
Development/
├── raghu-nayak.github.io/
├── au-fire-calculator/
└── investment-growth-calculator/
```

Override with `--fire PATH` / `--inv PATH`. Each page is loaded with its theme forced
through `localStorage` before first paint, screenshotted at 1440×1310, shrunk to 860px
wide, and written back into the four `--sf-*` / `--si-*` custom properties in
`index.html` at roughly 35 KB each.

## Adding a third calculator

1. Copy a `<article class="card">` block in `index.html` and rewrite the heading,
   tagline, four bullets, tags and two links.
2. Add a `--sx-d` / `--sx-l` pair to the token block, a `--shot-x` mapping in each
   theme, and a `.shot.x{background-image:var(--shot-x)}` rule.
3. Add the two entries to `TARGETS` in `tools/shots.py`, then run it.

The card grid is `1fr` below 960px and `1fr 1fr` above it; a third card wraps onto a
new row on its own, so widen the breakpoint to three columns if that looks wrong.

## Licence

[mortgage.monster](https://mortgage.monster/).
