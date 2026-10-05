import json
from pathlib import Path
import tempfile
import unittest
from tools.cover_assets import reviewed_cover, audit_reviewed_covers


class CoverAssetsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'data').mkdir()
        (self.root / 'static/images').mkdir(parents=True)

    def cover(self, content, reviewed=True, url='/images/test.svg'):
        (self.root / 'static/images/test.svg').write_text(content, encoding='utf-8')
        (self.root / 'data/reviewed_covers.json').write_text(json.dumps({
            'test': {'reviewed': reviewed, 'image': url}}), encoding='utf-8')
        return reviewed_cover(self.root, 'test')

    def test_static_svg_and_unknown_slug(self):
        self.assertEqual('/images/test.svg', self.cover(
            '<svg xmlns="http://www.w3.org/2000/svg"><text>Check export</text></svg>'))
        self.assertIsNone(reviewed_cover(self.root, 'unknown'))

    def test_rejects_active_or_external_content(self):
        for content in ['<script>alert(1)</script>', '<foreignObject/>',
                        '<image href="https://example.com/a.png"/>',
                        '<rect onclick="alert(1)"/>', '<rect fill="url(https://example.com/a)"/>']:
            with self.subTest(content=content), self.assertRaises(ValueError):
                self.cover('<svg xmlns="http://www.w3.org/2000/svg">'+content+'</svg>')

    def test_rejects_unreviewed_and_path_escape(self):
        with self.assertRaises(ValueError):
            self.cover('<svg/>', reviewed=False)
        with self.assertRaises(ValueError):
            self.cover('<svg/>', url='/images/../../test.svg')

    def test_rejects_malformed_and_entity_declarations(self):
        for content in ['<svg', '<!DOCTYPE svg><svg xmlns="http://www.w3.org/2000/svg"/>']:
            with self.subTest(content=content), self.assertRaises(ValueError):
                self.cover(content)

    def test_article_reference_mismatch_and_missing_article(self):
        self.cover('<svg xmlns="http://www.w3.org/2000/svg"/>')
        with self.assertRaises(ValueError):
            audit_reviewed_covers(self.root)
        posts = self.root / 'content/posts'
        posts.mkdir(parents=True)
        article = posts / 'test.md'
        article.write_text('---\nslug: "test"\ncover:\n  image: "/images/wrong.svg"\n---\n', encoding='utf-8')
        with self.assertRaises(ValueError):
            audit_reviewed_covers(self.root)
        article.write_text('---\nslug: "test"\ncover:\n  image: "/images/test.svg"\n---\n', encoding='utf-8')
        self.assertEqual(1, len(audit_reviewed_covers(self.root)))
        (posts / 'old-draft.md').write_text('---\nslug: "test"\ndraft: true\ncover:\n  image: "/images/old.svg"\n---\n', encoding='utf-8')
        self.assertEqual(1, len(audit_reviewed_covers(self.root)))


if __name__ == '__main__':
    unittest.main()
