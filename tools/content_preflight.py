"""Read-only publication inventory used before any paid draft generation."""
import re
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path


def inventory(posts_dir, today):
    slugs = set()
    published_today = []
    for path in Path(posts_dir).glob('*.md'):
        text = path.read_text(encoding='utf-8')
        if text.startswith('{'):
            fields, _ = json.JSONDecoder().raw_decode(text)
        elif text.startswith('---'):
            parts = text.split('---', 2)
            if len(parts) != 3:
                continue
            fields = dict(re.findall(r'^([a-z]+):\s*(.*?)\s*$', parts[1], re.M))
        else:
            continue
        slug = str(fields.get('slug', '')).strip('"\'')
        if slug:
            slugs.add(slug)
        date_raw = str(fields.get('date', '')).strip('"\'')
        date = date_raw[:10]
        if 'T' in date_raw:
            parsed = datetime.fromisoformat(date_raw.replace('Z', '+00:00'))
            if parsed.tzinfo is not None:
                date = parsed.astimezone(timezone(timedelta(hours=7))).date().isoformat()
        if date == today and str(fields.get('draft', 'false')).lower() != 'true':
            published_today.append(path.name)
    return {'slugs': slugs, 'published_today': published_today}


def eligible_candidates(posts_dir, today, articles):
    state = inventory(posts_dir, today)
    candidates = [a for a in articles if a['slug'] not in state['slugs']]
    if state['published_today']:
        candidates = []
    return state, candidates[:1]
