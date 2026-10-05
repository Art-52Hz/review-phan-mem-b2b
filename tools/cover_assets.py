"""Select reviewed editorial covers without generating images or calling APIs."""
import json
from pathlib import Path
import xml.etree.ElementTree as ET


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
