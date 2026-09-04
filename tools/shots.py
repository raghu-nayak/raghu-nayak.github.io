#!/usr/bin/env python3
"""Rebuild the card previews on the landing page.

Each calculator is screenshotted in both themes, shrunk to 860px and inlined
into index.html as a WebP data URI, so the page still makes no network
requests. Run this whenever either calculator changes visibly.

    python3 tools/shots.py

Needs Google Chrome and cwebp (`brew install webp`). Paths to the two
calculators can be overridden:

    python3 tools/shots.py --fire ../au-fire-calculator/index.html
"""
import argparse, base64, io, os, pathlib, re, shutil, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent.parent
PAGE = HERE / 'index.html'
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
WIDTH, HEIGHT, SCALED, QUALITY = 1440, 1310, 860, 80

# var name -> (source, localStorage theme key, theme)
TARGETS = {
    'sf-d': ('fire', 'aufire.theme', 'dark'),
    'sf-l': ('fire', 'aufire.theme', 'light'),
    'si-d': ('inv',  'igc.theme',    'dark'),
    'si-l': ('inv',  'igc.theme',    'light'),
    'sl-d': ('lev',  'alc.theme',    'dark'),
    'sl-l': ('lev',  'alc.theme',    'light'),
}


def shoot(src, key, theme, work):
    """A screenshot of src forced into the given theme, as WebP bytes."""
    html = io.open(src, encoding='utf-8').read()
    anchor = '<meta charset="utf-8">'
    if anchor not in html:
        sys.exit('no charset meta to hook the theme onto in %s' % src)
    # before the pre-paint script, so the page never renders the other theme
    html = html.replace(anchor, anchor + '\n<script>try{localStorage.setItem('
                        '"%s","%s");}catch(e){}</script>' % (key, theme), 1)
    page = work / ('%s-%s.html' % (src.stem, theme))
    io.open(page, 'w', encoding='utf-8').write(html)
    png, webp = work / 'shot.png', work / 'shot.webp'
    subprocess.run([CHROME, '--headless', '--disable-gpu', '--no-sandbox',
                    '--hide-scrollbars', '--virtual-time-budget=6000',
                    '--window-size=%d,%d' % (WIDTH, HEIGHT),
                    '--screenshot=%s' % png, page.as_uri()],
                   check=True, capture_output=True)
    if not png.exists():
        sys.exit('Chrome produced no screenshot for %s' % page)
    subprocess.run(['cwebp', '-resize', str(SCALED), '0', '-q', str(QUALITY),
                    '-m', '6', '-quiet', str(png), '-o', str(webp)], check=True)
    return webp.read_bytes()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--fire', default=str(HERE.parent / 'au-fire-calculator' / 'index.html'))
    ap.add_argument('--inv', default=str(HERE.parent / 'investment-growth-calculator' / 'index.html'))
    ap.add_argument('--lev', default=str(HERE.parent / 'au-leverage-calculator' / 'index.html'))
    args = ap.parse_args()
    if not shutil.which('cwebp'):
        sys.exit('cwebp not found — brew install webp')
    if not os.path.exists(CHROME):
        sys.exit('Google Chrome not found at %s' % CHROME)
    srcs = {'fire': pathlib.Path(args.fire), 'inv': pathlib.Path(args.inv),
            'lev': pathlib.Path(args.lev)}
    for name, path in srcs.items():
        if not path.exists():
            sys.exit('%s calculator not found at %s' % (name, path))

    page = io.open(PAGE, encoding='utf-8').read()
    with tempfile.TemporaryDirectory() as tmp:
        work = pathlib.Path(tmp)
        for var, (which, key, theme) in TARGETS.items():
            blob = shoot(srcs[which], key, theme, work)
            uri = 'url("data:image/webp;base64,%s")' % base64.b64encode(blob).decode('ascii')
            pat = re.compile(r'(  --%s:)url\("data:image/webp;base64,[^"]*"\);' % var)
            if not pat.search(page):
                sys.exit('could not find --%s in index.html' % var)
            page = pat.sub(lambda m: m.group(1) + uri + ';', page, count=1)
            print('  %-5s %s %-5s %6d bytes' % (var, which, theme, len(blob)))
    io.open(PAGE, 'w', encoding='utf-8').write(page)
    print('index.html rewritten: %d bytes' % len(page))


if __name__ == '__main__':
    main()
