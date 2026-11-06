import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location(
    "prepare_flatpark", Path(__file__).resolve().parents[1] / "scripts/prepare-flatpark.py"
)
packager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(packager)


class ReleaseIntegrityTest(unittest.TestCase):
    def generate(self, destination, corrupt=False):
        import hashlib

        payload = b"release payload"
        digest = hashlib.sha256(payload).hexdigest()
        url = f"https://github.com/{packager.REPO}/releases/download/v1/{packager.ASSET}"
        sums_url = f"https://github.com/{packager.REPO}/releases/download/v1/SHA256SUMS"
        release = {
            "draft": False, "prerelease": False, "published_at": "2026-11-06T12:00:00Z",
            "assets": [
                {"name": packager.ASSET, "browser_download_url": url, "size": len(payload)},
                {"name": "SHA256SUMS", "browser_download_url": sums_url},
            ],
        }
        responses = {
            f"https://api.github.com/repos/{packager.REPO}/releases/tags/v1": json.dumps(release).encode(),
            sums_url: f"{digest}  ./{packager.ASSET}\n".encode(),
            url: b"tampered content" if corrupt else payload,
        }
        with patch.object(packager, "fetch", side_effect=lambda address: io.BytesIO(responses[address])):
            with patch.object(sys, "argv", ["prepare-flatpark.py", "--tag", "v1", "--output", str(destination)]):
                packager.main()
        return digest

    def test_pins_match_verified_asset(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / packager.APP_ID
            digest = self.generate(destination)
            manifest = (destination / f"{packager.APP_ID}.yml").read_text()
            self.assertIn(digest, manifest)
            self.assertNotIn("@SHA256@", manifest)
            self.assertIn('version="1" date="2026-11-06"',
                          (destination / f"{packager.APP_ID}.metainfo.xml").read_text())
            self.assertTrue((destination / "apply_extra.sh").stat().st_mode & 0o111)

    def test_corruption_leaves_no_package(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / packager.APP_ID
            with self.assertRaisesRegex(ValueError, "mismatch"):
                self.generate(destination, corrupt=True)
            self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
