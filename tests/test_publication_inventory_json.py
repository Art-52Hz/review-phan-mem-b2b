import json
from pathlib import Path
import tempfile
import unittest
from tools.content_preflight import inventory


class JsonInventoryTests(unittest.TestCase):
    def test_json_utc_timestamp_counts_vietnam_publication_day(self):
        with tempfile.TemporaryDirectory() as folder:
            Path(folder, 'article.md').write_text(json.dumps({
                'slug': 'real-article', 'draft': False,
                'date': '2026-10-02T18:00:00Z'}) + '\nContent', encoding='utf8')
            state = inventory(folder, '2026-10-03')
            self.assertEqual(state['published_today'], ['article.md'])
            self.assertIn('real-article', state['slugs'])
            self.assertEqual(inventory(folder, '2026-10-02')['published_today'], [])

    def test_json_draft_never_consumes_publication_limit(self):
        with tempfile.TemporaryDirectory() as folder:
            Path(folder, 'draft.md').write_text(json.dumps({
                'slug': 'draft-article', 'draft': True,
                'date': '2026-10-03'}), encoding='utf8')
            state = inventory(folder, '2026-10-03')
            self.assertEqual(state['published_today'], [])
            self.assertIn('draft-article', state['slugs'])
