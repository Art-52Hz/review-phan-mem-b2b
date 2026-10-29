import json
import unittest
from pathlib import Path
from datetime import date
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
class VPSPricesTests(unittest.TestCase):
    def test_verified_sources_and_prices(self):
        plans = json.loads((ROOT / "data/vps-prices.json").read_text())["plans"]
        self.assertTrue(plans)
        self.assertEqual({p["provider"] for p in plans}, {"Hostinger", "UltaHost", "Contabo"})
        self.assertEqual(len(plans),len({p["id"] for p in plans}))
        for p in plans:
            with self.subTest(plan=p["id"]):
                self.assertIn(urlsplit(p["source_url"]).hostname, ["www.hostinger.com", "ultahost.com", "contabo.com"])
                self.assertEqual(urlsplit(p["source_url"]).scheme,"https")
                date.fromisoformat(p["checked"])
                self.assertGreater(p["monthly_usd"], 0)
                self.assertGreater(p["ram_gb"],0)
                self.assertEqual(p["term_months"],24)
                self.assertIn(p["os"],["Linux","Windows"])
                if p["renewal_monthly_usd"] is not None: self.assertGreater(p["renewal_monthly_usd"],0)
    def test_known_invoice_and_renewal(self):
        plans=json.loads((ROOT / "data/vps-prices.json").read_text())["plans"]
        entry=next(p for p in plans if p["provider"]=="Hostinger" and p["name"]=="KVM 1")
        self.assertAlmostEqual(entry["monthly_usd"]*entry["term_months"],155.76)
        self.assertAlmostEqual(entry["renewal_monthly_usd"]*24,287.76)
        self.assertTrue(all(p["renewal_monthly_usd"] is None for p in plans if p["provider"]=="Contabo"))
