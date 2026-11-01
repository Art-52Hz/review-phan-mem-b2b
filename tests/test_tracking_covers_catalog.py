"""Moi chuong trinh trong affiliate-catalog phai duoc affiliate-tracking.js dem click (affiliate_click)."""
import json
import re
import unittest
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]


class TrackingCoversCatalog(unittest.TestCase):
    def test_every_catalog_host_is_tracked(self):
        catalog = json.loads((ROOT / "data/affiliate-catalog.json").read_text(encoding="utf-8"))
        script = (ROOT / "static/js/affiliate-tracking.js").read_text(encoding="utf-8")
        tracked = set(re.findall(r'"([a-z0-9.-]+\.[a-z]+)":\s*"[a-z0-9]+"', script))
        for record in catalog["records"]:
            host = urlparse(record["referral_url"]).hostname
            self.assertIn(host, tracked, f"{host} co trong catalog nhung khong duoc dem affiliate_click")


if __name__ == "__main__":
    unittest.main()
