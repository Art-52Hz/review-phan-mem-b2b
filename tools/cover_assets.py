"""Select reviewed editorial covers without generating images or calling APIs."""
import json
from pathlib import Path


def reviewed_cover(repo_path, slug):
    root = Path(repo_path).resolve()
    manifest = root / 'data' / 'reviewed_covers.json'
    if not manifest.exists():
        return None
    entry = json.loads(manifest.read_text(encoding='utf-8')).get(slug)
    if entry is None:
        return None
    if entry.get('reviewed') is not True:
        raise ValueError('Cover is not reviewed')
    url = entry['image']
    if not url.startswith('/images/') or '\\' in url or '?' in url or '#' in url:
        raise ValueError('Cover must use a local image URL')
    images = (root / 'static' / 'images').resolve()
    asset = (root / 'static' / url.lstrip('/')).resolve()
    if images not in asset.parents or asset.suffix.lower() not in {'.webp', '.png', '.jpg'}:
        raise ValueError('Invalid cover path')
    if not asset.is_file():
        raise FileNotFoundError(asset)
    return url
