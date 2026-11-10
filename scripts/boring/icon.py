#!/usr/bin/env python3
"""Print the css line for a Lucide icon, for the plain theme.

usage: scripts/boring/icon.py path/to/icon.svg [more.svg ...]

Get the svg files from https://lucide.dev (or the npm package lucide-static).
Put the printed lines into the `html.f {` block of copyparty/web/browser.css
(or the stylesheet of the page that needs the icon), then use the icon with
    --i: var(--i-NAME);
on an element that the theme draws as a mask (see `html.f #ops a:before`).
"""
import re
import sys
from pathlib import Path
from urllib.parse import quote

for arg in sys.argv[1:]:
    p = Path(arg)
    body = re.search(r"<svg[^>]*>(.*)</svg>", p.read_text(), re.S).group(1)
    body = re.sub(r"\s+", " ", body).strip().replace(" />", "/>").replace("> <", "><")
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#000" '
        'stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">' + body + "</svg>"
    )
    print('\t--i-%s: url("data:image/svg+xml,%s");' % (p.stem, quote(svg, safe="/:=' ")))
