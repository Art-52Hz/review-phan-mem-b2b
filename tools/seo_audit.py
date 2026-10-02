"""Audit a built Hugo site without network requests or fabricated analytics."""
import json
import sys
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.links = []; self.images = []; self.schemas = []; self.buffer = None
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'a': self.links.append(a.get('href', ''))
        if tag == 'img': self.images.append(a.get('src', ''))
        if tag == 'script' and a.get('type') == 'application/ld+json': self.buffer = ''
    def handle_data(self, text):
        if self.buffer is not None: self.buffer += text
    def handle_endtag(self, tag):
        if tag == 'script' and self.buffer is not None:
            self.schemas.append(json.loads(self.buffer)); self.buffer = None

def audit(root):
    errors = []; count = 0
    for path in root.rglob('*.html'):
        p = Page(); count += 1
        try: p.feed(path.read_text(encoding='utf-8'))
        except (ValueError, UnicodeError) as exc: errors.append(f'{path.relative_to(root)}: {exc}'); continue
        for link in p.links + p.images:
            u = urlsplit(link)
            if u.netloc not in ('', 'aiprofreelancer.com') or u.scheme not in ('', 'https', 'http'): continue
            if not u.path.startswith('/'): continue
            target = root / unquote(u.path).lstrip('/')
            if not target.exists() and not (target / 'index.html').exists():
                errors.append(f'{path.relative_to(root)} -> {u.path}')
    return {'html_pages': count, 'broken_local_references': sorted(set(errors))}

if __name__ == '__main__':
    result = audit(Path(sys.argv[1])); print(json.dumps(result, indent=2)); sys.exit(bool(result['broken_local_references']))
