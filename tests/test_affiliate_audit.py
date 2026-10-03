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


if __name__ == '__main__':
    unittest.main()
