import json
import tempfile
import unittest
from pathlib import Path

from src.file_integrity import build_manifest, verify_manifest, write_manifest


class FileIntegrityTests(unittest.TestCase):
    def test_manifest_is_sorted_and_excludes_manifest(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "b.txt").write_text("bravo", encoding="utf-8")
            (root / "a.txt").write_text("alpha", encoding="utf-8")
            manifest_path = root / "manifest.json"

            write_manifest(root, manifest_path)
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

            self.assertEqual(list(manifest), ["a.txt", "b.txt"])
            self.assertNotIn("manifest.json", manifest)

    def test_verify_detects_changed_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            monitored = root / "example.txt"
            monitored.write_text("original", encoding="utf-8")
            manifest_path = root / "manifest.json"

            write_manifest(root, manifest_path)
            self.assertEqual(verify_manifest(root, manifest_path), 0)

            monitored.write_text("changed", encoding="utf-8")
            self.assertEqual(verify_manifest(root, manifest_path), 1)

    def test_build_manifest_uses_relative_paths(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            nested = root / "nested"
            nested.mkdir()
            (nested / "example.txt").write_text("data", encoding="utf-8")

            self.assertEqual(list(build_manifest(root)), ["nested/example.txt"])


if __name__ == "__main__":
    unittest.main()
