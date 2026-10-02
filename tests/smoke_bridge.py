"""Retained offline demo; synthetic source, never import into the live website."""
import json
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, 'D:/CBOS')
sys.path.insert(0, 'D:/CBOS/tests')
import test_review_bundle as fixtures
from core.kernel.review_export import export_review_bundle

site = Path(__file__).resolve().parents[1]
output = Path(sys.argv[1]).absolute()
output.mkdir(exist_ok=False)
factory = fixtures.ReviewBundleTest()
factory.setUp()
try:
    source = export_review_bundle(factory.bundle(), output)
finally:
    factory.tearDown()
result = subprocess.run([sys.executable, '-B', str(site / 'cbos_bridge.py'), 'stage',
                         '--bundle', str(source), '--output', str(output),
                         '--slug', 'offline-fixture-review', '--allow-fixture'],
                        cwd=site, capture_output=True, text=True, encoding='utf-8', check=True)
staged = json.loads(result.stdout)
package = Path(staged['package'])
overlay = output / 'smoke-config.json'
overlay.write_text(json.dumps({'staticDir': [str(site / 'static'), str(package / 'static')]}), encoding='utf-8')
built = subprocess.run(['hugo', '--buildDrafts', '--contentDir', str(package / 'content'),
                        '--config', str(site / 'hugo.toml') + ',' + str(overlay),
                        '--destination', str(output / 'preview')], cwd=site,
                       capture_output=True, text=True, encoding='utf-8', errors='replace', check=True)
html = output / 'preview/posts/offline-fixture-review/index.html'
if not html.is_file() or 'DỮ LIỆU THỬ NGHIỆM' not in html.read_text(encoding='utf-8'):
    raise RuntimeError('Hugo fixture render not verified')
for asset in (package / 'static/images/cbos').iterdir():
    if (output / 'preview/images/cbos' / asset.name).read_bytes() != asset.read_bytes():
        raise RuntimeError('Hugo image render copy not verified')
page = html.read_text(encoding='utf-8')
if 'data-affiliate' not in page or 'affiliate-tracking.js' not in page:
    raise RuntimeError('Affiliate marker/tracking script missing from actual Hugo render')
record = {'fixture': True, 'published': False, 'source': str(source),
          'staged': staged, 'rendered': str(html), 'hugo_render_verified': True}
(output / 'SMOKE_RESULT.json').write_text(json.dumps(record, indent=2), encoding='utf-8')
print(json.dumps(record, indent=2))
