import tempfile
import unittest
from pathlib import Path
from tools.content_preflight import eligible_candidates, inventory


class ContentPreflightTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)
    def write(self, name, slug, date='2026-10-01', draft='false', lastmod='2026-10-02'):
        (self.root/name).write_text(f'---\nslug: "{slug}"\ndate: {date}\nlastmod: {lastmod}\ndraft: {draft}\n---\nText',encoding='utf-8')
    def test_existing_slug_blocks_duplicate_on_a_new_date(self):
        self.write('old.md','same')
        _, choices=eligible_candidates(self.root,'2026-10-02',[{'slug':'same'}])
        self.assertEqual(choices,[])
    def test_draft_slug_also_blocks_duplicate(self):
        self.write('draft.md','same',draft='true')
        _, choices=eligible_candidates(self.root,'2026-10-02',[{'slug':'same'}])
        self.assertEqual(choices,[])
    def test_one_live_article_blocks_generation_today(self):
        self.write('live.md','published','2026-10-02T11:00:00+07:00')
        _, choices=eligible_candidates(self.root,'2026-10-02',[{'slug':'new'}])
        self.assertEqual(choices,[])
    def test_refresh_is_not_a_new_publication(self):
        self.write('old.md','old',lastmod='2026-10-02')
        state, choices=eligible_candidates(self.root,'2026-10-02',[{'slug':'new'}])
        self.assertEqual(state['published_today'],[])
        self.assertEqual(choices,[{'slug':'new'}])
    def test_at_most_one_candidate(self):
        _,choices=eligible_candidates(self.root,'2026-10-02',[{'slug':'a'},{'slug':'b'}])
        self.assertEqual(choices,[{'slug':'a'}])
    def test_today_draft_does_not_count_as_publication(self):
        self.write('draft.md','draft','2026-10-02',draft='true')
        self.assertEqual(inventory(self.root,'2026-10-02')['published_today'],[])

if __name__=='__main__':
    unittest.main()
