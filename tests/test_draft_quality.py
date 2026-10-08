import ast
from datetime import datetime, timezone, timedelta
from pathlib import Path
import os
import tempfile
import unittest

from tools.draft_quality import DraftReviewRequired, validate_generated_draft


class DraftQualityTests(unittest.TestCase):
    def test_rejects_legacy_review_scores_and_metadata(self):
        for draft in ('Score: **4.6 / 5**', '4.4/5', 'Rating: 4 out of 5',
                      '4.8 stars', 'rating: "4.6"', '"ratingValue": 4.6'):
            with self.subTest(draft=draft), self.assertRaises(DraftReviewRequired):
                validate_generated_draft(draft)

    def test_rejects_invented_first_person_experience(self):
        for draft in ('We tested it for two months.', 'I personally used it.',
                      'We have extensively benchmarked this platform.'):
            with self.subTest(draft=draft), self.assertRaises(DraftReviewRequired):
                validate_generated_draft(draft)

    def test_accepts_planning_numbers_without_treating_them_as_ratings(self):
        draft = ('Proposed exercise, not a completed experiment: create 5 sample '
                 'records. Compare 3 plans and record costs. REVIEW REQUIRED: pricing.')
        self.assertEqual(draft, validate_generated_draft(draft))

    def test_empty_output_cannot_be_saved(self):
        for value in ('', '  ', None):
            with self.subTest(value=value), self.assertRaises(DraftReviewRequired):
                validate_generated_draft(value)

    def test_writer_rejects_before_creating_article_or_directory(self):
        # Load only the save function: do not import credentials or call the API.
        source = Path(__file__).resolve().parents[1] / 'tudong_gemini.py'
        tree = ast.parse(source.read_text(encoding='utf-8'))
        function = next(n for n in tree.body
                        if isinstance(n, ast.FunctionDef) and n.name == 'save_to_markdown')
        module = ast.Module(body=[function], type_ignores=[])
        with tempfile.TemporaryDirectory() as folder:
            posts = Path(folder) / 'not-created'
            namespace = dict(os=os, datetime=datetime, timezone=timezone,
                             timedelta=timedelta, POSTS_DIR=str(posts),
                             validate_generated_draft=validate_generated_draft)
            exec(compile(module, str(source), 'exec'), namespace)
            with self.assertRaises(DraftReviewRequired):
                namespace['save_to_markdown']('Review', 'review', 'Score: 4.6/5',
                                              'review', '/images/cover.svg')
            self.assertFalse(posts.exists())


if __name__ == '__main__':
    unittest.main()
