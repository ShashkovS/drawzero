#!/usr/bin/env python3
"""Check generated documentation links, image paths, and hidden API names."""
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1] / 'site'
LEGACY = re.compile(r'\b(get_keys_pressed|keys_mods_pressed|get_mouse_pressed|mouse_pos|keysdown|keysup|mousemotions|mousebuttonsdown|mousebuttonsup)\b|K\.MOD_')


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.links = []
        self.ids = set()
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs: self.ids.add(attrs['id'])
        for key in ('href', 'src'):
            if key in attrs: self.links.append(attrs[key])


def check():
    pages = {p.resolve(): Page(p) for p in ROOT.rglob('*.html')}
    errors = []
    for path, page in pages.items():
        if LEGACY.search(path.read_text()): errors.append(str(path) + ': hidden API name')
        for link in page.links:
            url = urlsplit(link)
            if url.scheme or url.netloc or link.startswith('data:'): continue
            target = ((ROOT / unquote(url.path).lstrip('/')) if url.path.startswith('/') else
                      path.parent / unquote(url.path)) if url.path else path
            if target.is_dir(): target /= 'index.html'
            target = target.resolve()
            if not target.exists(): errors.append(str(path) + ': missing ' + link)
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                errors.append(str(path) + ': missing anchor ' + link)
    for search in ROOT.rglob('search_index.json'):
        if LEGACY.search(search.read_text()): errors.append(str(search) + ': hidden API name')
    if errors: raise SystemExit('\n'.join(errors))
    print('Checked {} HTML pages, images, local links/anchors, and search indexes'.format(len(pages)))


if __name__ == '__main__': check()
