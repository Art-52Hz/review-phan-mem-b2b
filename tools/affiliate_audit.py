"""Compare rendered affiliate links with account-issued catalog URLs, offline."""
import argparse
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, parse_qsl


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.links.append(dict(attrs))


def account_key(url):
    parts = urlsplit(url)
    return parts.scheme, parts.hostname, parts.path.rstrip('/'), parts.fragment


def audit(build, catalog):
    records = catalog['records']
    expected = {account_key(r['referral_url']): r['program_id']
                for r in records if r.get('referral_url')}
    hosts = {key[1] for key in expected}
    errors = []
    occurrences = {r['program_id']: 0 for r in records}
    for page in sorted(Path(build).rglob('*.html')):
        parser = Links()
        parser.feed(page.read_text(encoding='utf-8'))
        for link in parser.links:
            href = link.get('href', '')
            key = account_key(href)
            location = page.relative_to(build).as_posix()
            # Explicit affiliate markers require an issued catalog URL even
            # when the destination belongs to a previously unseen vendor.
            if link.get('data-affiliate') == 'true' and key not in expected:
                errors.append({'page': location, 'problem': 'uncatalogued affiliate URL', 'host': key[1]})
                continue
            # Shared vendor domains also contain ordinary product/help links.
            is_candidate = key[1] in hosts and (
                (key[1] != 'mangools.com' or key[3].startswith('a')) and
                (key[1] != 'ultahost.com' or bool(key[3]) or
                 link.get('data-affiliate') == 'true'))
            if not is_candidate:
                continue
            if key not in expected:
                errors.append({'page': location, 'problem': 'account URL mismatch', 'host': key[1]})
                continue
            # Only the existing ElevenLabs editorial ref labels are recognized.
            allowed_query_keys = {'ref'} if expected[key] == 'elevenlabs' else set()
            if any(name not in allowed_query_keys for name, _ in parse_qsl(urlsplit(href).query)):
                errors.append({'page': location, 'problem': 'unreviewed referral query', 'program': expected[key]})
            occurrences[expected[key]] += 1
            rel = set(link.get('rel', '').split())
            required = {'sponsored', 'noopener'}
            if expected[key] == 'murf':
                if 'noreferrer' in rel or link.get('referrerpolicy') != 'strict-origin':
                    errors.append({'page': location, 'problem': 'Murf requires origin-only referral policy', 'program': 'murf'})
            else:
                required.add('noreferrer')
            if link.get('data-affiliate') != 'true' or not required <= rel:
                errors.append({'page': location, 'problem': 'missing tracking/sponsored markers', 'program': expected[key]})
    return {'scope': 'rendered local build; not redirect, attribution or revenue verification',
            'missing_catalog_links': [r['program_id'] for r in records if not r.get('referral_url')],
            'rendered_link_occurrences': occurrences, 'errors': errors}


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('build', type=Path)
    cli.add_argument('--catalog', type=Path, default=Path(__file__).resolve().parents[1] / 'data' / 'affiliate-catalog.json')
    args = cli.parse_args()
    result = audit(args.build, json.loads(args.catalog.read_text(encoding='utf-8')))
    print(json.dumps(result, indent=2))
    raise SystemExit(bool(result['errors'] or result['missing_catalog_links']))
