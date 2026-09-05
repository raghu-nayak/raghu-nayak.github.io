# raghu-nayak.github.io

The landing page at **[raghu-nayak.github.io](https://raghu-nayak.github.io/)** — one
self-contained HTML file that lists the calculators, built from the same design tokens
they use so every page reads as one thing.

No build step, no dependencies, no network requests: the card previews are real
screenshots of each tool, inlined as WebP data URIs, in both light and dark.

## What it links to

| Calculator | Live | Source |
| --- | --- | --- |
| **Australian FIRE Calculator** — the earliest you could stop working, with super and everything outside it modelled apart | [open](https://raghu-nayak.github.io/au-fire-calculator/) | [repo](https://github.com/raghu-nayak/au-fire-calculator) |
| **Investment Growth Calculator** — what contributions, returns, fees, tax and inflation do to a portfolio | [open](https://raghu-nayak.github.io/investment-calc/) | [repo](https://github.com/raghu-nayak/investment-calc) |
| **Debt Recycling &amp; Leverage Calculator** — borrowing to invest under Australian tax, measured against not borrowing | [open](https://raghu-nayak.github.io/au-leverage-calculator/) | [repo](https://github.com/raghu-nayak/au-leverage-calculator) |

## Run it locally

```sh
open index.html          # macOS
xdg-open index.html      # Linux
start index.html         # Windows
```

`file://` behaves exactly like `https://` — there is nothing to serve.

## Regenerating the previews

The screenshots go stale when any calculator changes. Rebuild all six:

```sh
python3 tools/shots.py
```

Needs Google Chrome and `cwebp` (`brew install webp`). It expects the calculators
checked out beside this repo:

```
Development/
├── raghu-nayak.github.io/
├── au-fire-calculator/
├── au-leverage-calculator/
└── investment-growth-calculator/
```

Override with `--fire PATH` / `--inv PATH` / `--lev PATH`. Each page is loaded with its
theme forced through `localStorage` before first paint, screenshotted at 1440×1310,
shrunk to 860px wide, and written back into the six `--sf-*` / `--si-*` / `--sl-*`
custom properties in `index.html` at roughly 35 KB each.

## Adding another calculator

1. Copy an `<article class="card">` block in `index.html` and rewrite the heading,
   tagline, four bullets, tags and two links.
2. Add a `--sx-d` / `--sx-l` pair to the token block (an empty
   `url("data:image/webp;base64,")` is a fine placeholder), a `--shot-x` mapping in
   each theme, and a `.shot.x{background-image:var(--shot-x)}` rule.
3. Add the two entries to `TARGETS` in `tools/shots.py` with the tool's own
   `localStorage` theme key, add its `--x` path argument, then run it.

The card grid is `repeat(auto-fit,minmax(360px,1fr))`, so it goes one-up, two-up and
three-up on its own as the page widens — no breakpoint to touch when the count
changes.

## Copyright

Copyright &copy; 2026 Raghu Nayak. All rights reserved. The colour palette is
taken from [mortgage.monster](https://mortgage.monster/).
