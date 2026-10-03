"""Operator-invoked CBOS -> Hugo executor. No model calls or implicit Git push."""
import argparse
from datetime import datetime, timezone, timedelta
import hashlib
import json
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile


class BridgeError(ValueError):
    pass


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def safe_path(path):
    path = Path(path).absolute()
    for parent in (path, *path.parents):
        if parent.exists() and (parent.is_symlink() or
                getattr(parent.lstat(), 'st_file_attributes', 0) &
                getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 1024)):
            raise BridgeError('Symlinks/junctions are not allowed')
    return path


def read_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise BridgeError('Duplicate JSON key')
            result[key] = value
        return result
    path = safe_path(path)
    if path.stat().st_size > 1024 * 1024:
        raise BridgeError('JSON exceeds 1 MiB')
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=pairs)


def verify_bundle(bundle_dir, cbos_root):
    root = safe_path(bundle_dir)
    cbos = safe_path(cbos_root)
    if str(cbos) not in sys.path:
        sys.path.insert(0, str(cbos))
    from core.kernel.review_export import content_from_dict
    from core.workflow.review_bundle import ReviewImage, build_review_bundle
    manifest = read_json(root / 'manifest.json')
    if not isinstance(manifest, dict) or manifest.get('schema_version') != 1:
        raise BridgeError('Unsupported CBOS manifest')
    images = []
    for image in manifest.get('images', []):
        name = image['file']
        if not re.fullmatch(r'assets/[0-9a-f]{64}\.(png|jpg)', name):
            raise BridgeError('Invalid asset path')
        asset = safe_path(root / name)
        if asset.stat().st_size > 5 * 1024 * 1024:
            raise BridgeError('Image exceeds 5 MiB')
        images.append(ReviewImage(product_id=image['product_id'], data=asset.read_bytes(),
                                  source_url=image['source_url'], rights=image['rights'],
                                  expected_sha256=image['sha256']))
    rebuilt = build_review_bundle(content_from_dict(manifest['content']), images=tuple(images),
                                 affiliate_links=manifest['affiliate_links'],
                                 affiliate_disclosure=manifest['affiliate_disclosure'],
                                 fixture=manifest['fixture'])
    if manifest != json.loads(rebuilt.files['manifest.json']):
        raise BridgeError('Manifest does not match rebuilt CBOS bundle')
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    if actual != set(rebuilt.files):
        raise BridgeError('Bundle file inventory mismatch')
    for name, raw in rebuilt.files.items():
        if safe_path(root / name).read_bytes() != raw:
            raise BridgeError('Bundle file changed: ' + name)
    return manifest, rebuilt


def stage(bundle_dir, cbos_root, output, slug, allow_fixture=False):
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug) or len(slug) > 100:
        raise BridgeError('Invalid Hugo slug')
    manifest, bundle = verify_bundle(bundle_dir, cbos_root)
    if bundle.status != 'READY_FOR_REVIEW':
        raise BridgeError('Incomplete content cannot be staged')
    if manifest['fixture'] and not allow_fixture:
        raise BridgeError('Fixture requires explicit opt-in')
    output = safe_path(output)
    if not output.is_dir():
        raise BridgeError('Output must be an existing directory')
    target = output / (slug + '-' + bundle.bundle_id)
    title = manifest['content']['title']
    # JSON front matter avoids YAML string injection. Every staged article is draft.
    front = {'title': title, 'slug': slug, 'date': datetime.now(timezone.utc).isoformat(),
             'draft': True, 'cbos_bundle_id': bundle.bundle_id,
             'cbos_fixture': manifest['fixture'], 'categories': ['Technology'],
             'tags': ['affiliate'], 'description': title}
    article = bundle.files['article.md'].decode('utf-8')
    files = {}
    for name, raw in bundle.files.items():
        if name.startswith('assets/'):
            destination = 'static/images/cbos/' + Path(name).name
            files[destination] = raw
            article = article.replace('(' + name + ')', '(/images/cbos/' + Path(name).name + ')')
    files['content/posts/' + slug + '.md'] = (json.dumps(front, ensure_ascii=False, indent=2)
                                            + '\n\n' + article).encode('utf-8')
    receipt = {'schema_version': 1, 'bundle_id': bundle.bundle_id, 'slug': slug,
               'fixture': manifest['fixture'], 'state': 'STAGED_DRAFT',
               'files': {name: digest(raw) for name, raw in sorted(files.items())}}
    encoded = json.dumps(receipt, sort_keys=True, ensure_ascii=False, indent=2).encode('utf-8')
    target.mkdir(exist_ok=False)
    for name, raw in files.items():
        path = target / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as stream:
            stream.write(raw)
    with (target / 'receipt.json').open('xb') as stream:
        stream.write(encoded)
    return target, digest(encoded)


def import_draft(package, site, approval_sha256):
    package, site = safe_path(package), safe_path(site)
    raw = safe_path(package / 'receipt.json').read_bytes()
    if digest(raw) != approval_sha256:
        raise BridgeError('Exact receipt approval hash required')
    receipt = read_json(package / 'receipt.json')
    if receipt.get('fixture') is not False or receipt.get('state') != 'STAGED_DRAFT':
        raise BridgeError('Only real staged drafts may enter the website')
    if not (site / 'hugo.toml').is_file() or not site.is_dir():
        raise BridgeError('Hugo website root required')
    expected = 'content/posts/' + receipt['slug'] + '.md'
    if expected not in receipt['files']:
        raise BridgeError('Missing article')
    files = {}
    for name, checksum in receipt['files'].items():
        if name != expected and not re.fullmatch(r'static/images/cbos/[0-9a-f]{64}\.(png|jpg)', name):
            raise BridgeError('Invalid package destination')
        if not re.fullmatch(r'content/posts/[a-z0-9]+(?:-[a-z0-9]+)*\.md', expected):
            raise BridgeError('Invalid article path')
        data = safe_path(package / name).read_bytes()
        if digest(data) != checksum:
            raise BridgeError('Changed package file')
        dest = safe_path(site / name)
        if dest.exists():
            if name == expected or dest.read_bytes() != data:
                raise BridgeError('Destination already exists')
        files[name] = data
    article = files[expected].decode('utf-8')
    front, _ = json.JSONDecoder().raw_decode(article)
    if front.get('draft') is not True or front.get('cbos_fixture') is not False:
        raise BridgeError('Imported article must be a real draft')
    for name, data in files.items():
        dest = safe_path(site / name)
        if dest.exists():
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open('xb') as stream:
            stream.write(data)
    return {'state': 'IMPORTED_DRAFT', 'bundle_id': receipt['bundle_id'],
            'files': list(files), 'published': False}


def publish(package, site, approval_sha256, journal_root):
    """Explicit exact-package publication; failed/unknown attempts never auto-retry."""
    package, site, journal = safe_path(package), safe_path(site), safe_path(journal_root)
    if not journal.is_dir() or journal == site or site in journal.parents:
        raise BridgeError('Journal must be an existing directory outside the site')
    if digest((package / 'receipt.json').read_bytes()) != approval_sha256:
        raise BridgeError('Exact receipt approval required')
    receipt = read_json(package / 'receipt.json')
    if receipt.get('fixture') is not False or receipt.get('state') != 'STAGED_DRAFT':
        raise BridgeError('Fixtures cannot be published')
    expected = 'content/posts/' + receipt['slug'] + '.md'
    if not re.fullmatch(r'content/posts/[a-z0-9]+(?:-[a-z0-9]+)*\.md', expected):
        raise BridgeError('Invalid article path')
    for name, checksum in receipt['files'].items():
        if name != expected and not re.fullmatch(r'static/images/cbos/[0-9a-f]{64}\.(png|jpg)', name):
            raise BridgeError('Invalid publication file')
        if digest(safe_path(site / name).read_bytes()) != checksum:
            raise BridgeError('Imported draft changed or missing')
    if expected not in receipt['files']:
        raise BridgeError('Missing article')
    def git(*args):
        result = subprocess.run(['git', *args], cwd=site, capture_output=True, text=True,
                                encoding='utf-8', errors='replace', timeout=120)
        if result.returncode:
            raise BridgeError('Git operation failed; inspect locally before retry')
        return result.stdout.strip()
    if git('branch', '--show-current') != 'main':
        raise BridgeError('Publication requires the existing main branch')
    if git('diff', '--cached', '--name-only'):
        raise BridgeError('Existing staged changes must be preserved')
    changed = set(git('diff', '--name-only').splitlines())
    if changed - set(receipt['files']):
        raise BridgeError('Unrelated tracked changes require inspection')
    # Prevent pushing earlier unpublished commits accidentally.
    local_head = git('rev-parse', 'HEAD')
    remote = git('ls-remote', 'origin', 'refs/heads/main').split()
    if not remote or remote[0] != local_head:
        raise BridgeError('Local and remote main must match before publication')
    article_path = safe_path(site / expected)
    text = article_path.read_text(encoding='utf-8')
    front, end = json.JSONDecoder().raw_decode(text)
    if front.get('draft') is not True or front.get('cbos_fixture') is not False:
        raise BridgeError('Expected a nonfixture draft')
    day = datetime.now(timezone(timedelta(hours=7))).date().isoformat()
    from tools.content_preflight import inventory
    if inventory(site / 'content/posts', day)['published_today']:
        raise BridgeError('A live article already exists for today; preserve the daily limit')
    attempt = journal / (day + '.json')
    # Atomic day reservation serializes cooperating executors, at most one attempt/day.
    entry = {'state': 'INTENT', 'bundle_id': receipt['bundle_id'],
             'approval_sha256': approval_sha256, 'base_head': local_head}
    with attempt.open('x', encoding='utf-8') as stream:
        json.dump(entry, stream)
    try:
        front['draft'] = False
        front['date'] = datetime.now(timezone.utc).isoformat()
        article_path.write_text(json.dumps(front, ensure_ascii=False, indent=2) + text[end:], encoding='utf-8')
        with tempfile.TemporaryDirectory(prefix='aipro-hugo-') as build:
            built = subprocess.run(['hugo', '--minify', '--buildFuture', '--destination', build],
                                   cwd=site, capture_output=True, text=True,
                                   encoding='utf-8', errors='replace', timeout=120)
            if built.returncode:
                raise BridgeError('Hugo build failed; inspect local output')
        git('add', '--', *receipt['files'])
        git('commit', '--only', '-m', 'Publish reviewed CBOS article: ' + receipt['slug'],
            '--', *receipt['files'])
        entry['commit'] = git('rev-parse', 'HEAD')
        entry['state'] = 'PUSH_INTENT'
        attempt.write_text(json.dumps(entry, indent=2), encoding='utf-8')
        git('push', 'origin', 'HEAD:refs/heads/main')
        entry['state'] = 'PUSHED_DEPLOY_PENDING'
        attempt.write_text(json.dumps(entry, indent=2), encoding='utf-8')
        return entry
    except Exception:
        entry['state'] = 'UNKNOWN_REQUIRES_INSPECTION'
        attempt.write_text(json.dumps(entry, indent=2), encoding='utf-8')
        raise


def main():
    parser = argparse.ArgumentParser(description='CBOS Article + Image -> Hugo local executor')
    commands = parser.add_subparsers(dest='command', required=True)
    prepare = commands.add_parser('stage')
    prepare.add_argument('--bundle', required=True)
    prepare.add_argument('--cbos-root', default='D:\\CBOS')
    prepare.add_argument('--output', required=True)
    prepare.add_argument('--slug', required=True)
    prepare.add_argument('--allow-fixture', action='store_true')
    receive = commands.add_parser('import-draft')
    receive.add_argument('--package', required=True)
    receive.add_argument('--site', default=str(Path(__file__).resolve().parent))
    receive.add_argument('--approve-sha256', required=True)
    send = commands.add_parser('publish')
    send.add_argument('--package', required=True)
    send.add_argument('--site', default=str(Path(__file__).resolve().parent))
    send.add_argument('--approve-sha256', required=True)
    send.add_argument('--journal', required=True)
    args = parser.parse_args()
    try:
        if args.command == 'stage':
            path, checksum = stage(args.bundle, args.cbos_root, args.output, args.slug, args.allow_fixture)
            print(json.dumps({'package': str(path), 'receipt_sha256': checksum, 'published': False}))
        elif args.command == 'import-draft':
            print(json.dumps(import_draft(args.package, args.site, args.approve_sha256)))
        else:
            print(json.dumps(publish(args.package, args.site, args.approve_sha256, args.journal)))
    except (ValueError, KeyError, TypeError, OSError, ImportError, subprocess.TimeoutExpired) as exc:
        parser.exit(2, 'Bridge rejected: ' + str(exc) + '\n')


if __name__ == '__main__':
    main()
