"""Read-only publication inventory used before any paid draft generation."""
import re
from pathlib import Path


def inventory(posts_dir, today):
    slugs = set()
    published_today = []
    for path in Path(posts_dir).glob('*.md'):
        text = path.read_text(encoding='utf-8')
        if not text.startswith('---'):
            continue
        parts = text.split('---', 2)
        if len(parts) != 3:
            continue
        fields = dict(re.findall(r'^([a-z]+):\s*(.*?)\s*$', parts[1], re.M))
        slug = fields.get('slug', '').strip('"\'')
        if slug:
            slugs.add(slug)
        date = fields.get('date', '').strip('"\'')[:10]
        if date == today and fields.get('draft', 'false').lower() != 'true':
            published_today.append(path.name)
    return {'slugs': slugs, 'published_today': published_today}


def eligible_candidates(posts_dir, today, articles):
    state = inventory(posts_dir, today)
    candidates = [a for a in articles if a['slug'] not in state['slugs']]
    if state['published_today']:
        candidates = []
    return state, candidates[:1]
