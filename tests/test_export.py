import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from export_public import export  # noqa: E402
from validate import inspect, split  # noqa: E402

NOW = datetime(2026, 11, 12, 15, 0, tzinfo=timezone.utc)


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.out = Path(self.tmp.name) / "okf"
        self.count = export(ROOT, self.out, NOW)

    def tearDown(self):
        self.tmp.cleanup()

    def test_exports_records(self):
        self.assertGreater(self.count, 10)
        self.assertTrue((self.out / "markets/en.md").exists())

    def test_root_index_declares_version_only(self):
        meta, _ = split((self.out / "index.md").read_text())
        self.assertEqual(meta, {"okf_version": "0.2"})

    def test_only_public_stable_verified(self):
        for p in self.out.rglob("*.md"):
            if p.name in ("index.md", "log.md"):
                continue
            meta, body = split(p.read_text())
            self.assertEqual(meta["audience"], "public", p)
            self.assertEqual(meta["status"], "stable", p)
            self.assertTrue(meta["verified"], p)
            self.assertNotIn("[NEEDS CONFIRMATION", body, p)

    def test_editorial_excluded(self):
        self.assertFalse((self.out / "competitors").exists())
        self.assertFalse((self.out / "internal").exists())
        self.assertFalse((self.out / "README.md").exists())

    def test_export_is_valid_and_links_resolve(self):
        errors, _, _ = inspect(self.out, NOW)
        self.assertEqual(errors, [])

    def test_manifest(self):
        manifest = json.loads((self.out / "manifest.json").read_text())
        self.assertEqual(manifest["okf_version"], "0.2")
        self.assertIn("competitors/tempstars.md", manifest["excluded"])

    def test_stale_records_drop_out(self):
        later = datetime(2027, 1, 1, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                export(ROOT, Path(tmp) / "okf", later)


if __name__ == "__main__":
    unittest.main()
