import tempfile
import unittest
from pathlib import Path
from tools.affiliate_audit import audit


class AffiliateAuditTests(unittest.TestCase):
    def check(self, html):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'index.html').write_text(html, encoding='utf-8')
            return audit(root, {'records': [{'program_id': 'elevenlabs', 'referral_url': 'https://try.elevenlabs.io/issued'}]})

    def test_account_path_mismatch_is_detected(self):
        result = self.check('<a href="https://try.elevenlabs.io/other-account">Buy</a>')
        self.assertEqual(result['errors'][0]['problem'], 'account URL mismatch')

    def test_missing_markers_are_detected(self):
        result = self.check('<a href="https://try.elevenlabs.io/issued">Buy</a>')
        self.assertEqual(result['errors'][0]['problem'], 'missing tracking/sponsored markers')

    def test_unknown_query_is_detected_but_editorial_ref_is_allowed(self):
        anchor = '<a href="https://try.elevenlabs.io/issued?{}" data-affiliate="true" rel="sponsored noopener noreferrer">Buy</a>'
        self.assertFalse(self.check(anchor.format('ref=article'))['errors'])
        self.assertEqual(self.check(anchor.format('affiliate=other-account'))['errors'][0]['problem'], 'unreviewed referral query')

    def test_murf_origin_only_policy_and_masking_regressions(self):
        catalog = {'records': [{'program_id': 'murf', 'referral_url': 'https://get.murf.ai/issued'}]}
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            page = root / 'index.html'
            for rel, policy, valid in [
                ('sponsored noopener', 'strict-origin', True),
                ('sponsored noopener noreferrer', 'strict-origin', False),
                ('sponsored noopener', 'unsafe-url', False),
                ('sponsored noopener', '', False),
            ]:
                with self.subTest(rel=rel, policy=policy):
                    page.write_text(f'<a href="https://get.murf.ai/issued" data-affiliate="true" rel="{rel}" referrerpolicy="{policy}">Murf</a>', encoding='utf-8')
                    result = audit(root, catalog)
                    self.assertEqual(not result['errors'], valid)
                    if not valid:
                        self.assertEqual(result['errors'][0]['problem'], 'Murf requires origin-only referral policy')


if __name__ == '__main__':
    unittest.main()
