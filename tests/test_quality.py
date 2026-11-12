import re
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate import inspect  # noqa: E402

NOW = datetime(2026, 11, 12, 15, 0, tzinfo=timezone.utc)


class QualityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.errors, cls.warnings, cls.records = inspect(ROOT, NOW)

    def test_no_validation_errors(self):
        self.assertEqual(self.errors, [])

    def test_required_folders_present(self):
        for folder in ["brand", "citations", "competitors", "concepts", "destinations", "docs", "evaluations",
                       "faq", "governance", "guides", "internal", "internal-links", "markets", "policies",
                       "products", "scripts", "tests"]:
            self.assertTrue((ROOT / folder).is_dir(), folder)

    def test_primary_reference_is_stable(self):
        meta, _ = self.records["markets/en.md"]
        self.assertEqual(meta["status"], "stable")
        self.assertTrue(meta["verified"])

    def test_editorial_records_are_not_public(self):
        for rel, (meta, _) in self.records.items():
            if rel.startswith(("competitors/", "internal/")):
                self.assertEqual(meta["audience"], "internal-editorial", rel)

    def test_no_human_actor_claimed(self):
        for rel, (meta, _) in self.records.items():
            for v in meta.get("verified") or []:
                self.assertFalse(str(v["by"]).startswith("human:"), f"{rel}: human review is not recorded yet")

    def test_no_2025_as_current_year(self):
        for rel, (_, body) in self.records.items():
            for line in body.splitlines():
                if re.search(r"\b2025\b", line):
                    self.assertRegex(line, r"(July 1, 2025|October 1, 2025|June 30, 2025|2025-06-30)", rel)


if __name__ == "__main__":
    unittest.main()
