from datetime import datetime, timedelta
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import testflight_ci_signing as signing


def profile(**extra):
    return {"TeamIdentifier": ["TEAM"], "UUID": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "ExpirationDate": datetime.now() + timedelta(days=1),
            "Entitlements": {"application-identifier": "TEAM.it.example.App", "get-task-allow": False}, **extra}


class SigningTests(unittest.TestCase):
    def test_profile_must_match_app_team_distribution_and_expiration(self):
        self.assertEqual(signing.profile_identity(profile(), "it.example.App", "TEAM"), "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
        for bad in [profile(TeamIdentifier=["OTHER"]), profile(ExpirationDate=datetime.now() - timedelta(days=1)),
                    profile(ProvisionedDevices=["device"]), profile(ProvisionsAllDevices=True),
                    profile(Entitlements={"application-identifier": "TEAM.other", "get-task-allow": False}),
                    profile(Entitlements={"application-identifier": "TEAM.it.example.App", "get-task-allow": True})]:
            with self.subTest(profile=bad), self.assertRaises(ValueError):
                signing.profile_identity(bad, "it.example.App", "TEAM")

    def test_missing_secret_stops_before_import_and_can_be_cleaned(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "signing"
            with patch.dict(os.environ, {}, clear=True), patch.object(signing, "run") as command:
                with self.assertRaises(ValueError): signing.prepare(folder)
                command.assert_not_called()
            signing.cleanup(folder)
            self.assertFalse(folder.exists())

    def test_cleanup_preserves_preexisting_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "signing"
            folder.mkdir()
            existing = Path(tmp) / "existing.mobileprovision"
            existing.write_bytes(b"existing")
            (folder / "state.json").write_text(json.dumps({"profile_created": False, "profile_path": str(existing)}))
            signing.cleanup(folder)
            self.assertEqual(existing.read_bytes(), b"existing")

    def test_cleanup_only_removes_its_unchanged_profile(self):
        for current in [b"ours", b"another job"]:
            with self.subTest(current=current), tempfile.TemporaryDirectory() as tmp:
                folder = Path(tmp) / "signing"
                folder.mkdir()
                target = Path(tmp) / "profile.mobileprovision"
                target.write_bytes(current)
                (folder / "App.mobileprovision").write_bytes(b"ours")
                (folder / "state.json").write_text(json.dumps({"profile_created": True, "profile_path": str(target)}))
                signing.cleanup(folder)
                self.assertEqual(target.exists(), current != b"ours")


if __name__ == "__main__":
    unittest.main()
