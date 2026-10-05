"""Select reviewed editorial covers without generating images or calling APIs."""
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import re


def _validate_svg(asset):
    """Accept static editorial SVG only, without scripts or linked resources."""
    source = asset.read_text(encoding='utf-8')
    if '<!DOCTYPE' in source.upper() or '<!ENTITY' in source.upper():
        raise ValueError('SVG declarations are not allowed')
    try:
        svg = ET.fromstring(source)
    except ET.ParseError as exc:
        raise ValueError('Invalid SVG') from exc
    allowed = {'svg', 'g', 'rect', 'circle', 'ellipse', 'path', 'line',
               'polyline', 'polygon', 'text', 'tspan', 'title', 'desc'}
    if svg.tag != '{http://www.w3.org/2000/svg}svg':
        raise ValueError('Invalid SVG root')
    for node in svg.iter():
        if node.tag not in {'{http://www.w3.org/2000/svg}' + name for name in allowed}:
            raise ValueError('Unsupported SVG element')
        for key, value in node.attrib.items():
            name = key.rsplit('}', 1)[-1].lower()
            if name.startswith('on') or name in {'href', 'src', 'style'} or 'url(' in value.lower():
                raise ValueError('Active or linked SVG content is not allowed')


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
    if images not in asset.parents or asset.suffix.lower() not in {'.webp', '.png', '.jpg', '.svg'}:
        raise ValueError('Invalid cover path')
    if not asset.is_file():
        raise FileNotFoundError(asset)
    if asset.suffix.lower() == '.svg':
        _validate_svg(asset)
    return url


def audit_reviewed_covers(repo_path):
    """Check declared reviewed covers and their matching article references."""
    root = Path(repo_path).resolve()
    manifest = root / 'data/reviewed_covers.json'
    if not manifest.is_file():
        raise FileNotFoundError(manifest)
    entries = json.loads(manifest.read_text(encoding='utf-8'))
    results = []
    for slug in entries:
        image = reviewed_cover(root, slug)
        articles = []
        for post in (root / 'content/posts').glob('*.md'):
            text = post.read_text(encoding='utf-8')
            if text.startswith('{'):
                fields, _ = json.JSONDecoder().raw_decode(text)
                if str(fields.get('draft', False)).lower() == 'true':
                    continue
                declared_slug = fields.get('slug', post.stem)
                declared_cover = fields.get('cover', {}).get('image')
            elif text.startswith('---'):
                front = text.split('---', 2)[1]
                if re.search(r'^draft:\s*[\"\']?true[\"\']?\s*$', front, re.M | re.I):
                    continue
                match = re.search(r'^slug:\s*[\"\']?([^\"\'\r\n]+)', front, re.M)
                declared_slug = match.group(1).strip() if match else post.stem
                cover = re.search(r'^cover:\s*\n(?:[ \t].*\n)*?[ \t]+image:\s*[\"\']?([^\"\'\r\n]+)', front, re.M)
                declared_cover = cover.group(1).strip() if cover else None
            else:
                continue
            if declared_slug != slug:
                continue
            if declared_cover != image:
                raise ValueError(f'Article cover differs from reviewed cover: {post.name}')
            articles.append(post.name)
        if not articles:
            raise ValueError(f'Reviewed cover has no matching article: {slug}')
        results.append({'slug': slug, 'image': image, 'articles': articles})
    return results


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repo', type=Path)
    args = parser.parse_args()
    print(json.dumps({'scope': 'Local reviewed-cover references only; no publishing',
                      'results': audit_reviewed_covers(args.repo)}, indent=2))
