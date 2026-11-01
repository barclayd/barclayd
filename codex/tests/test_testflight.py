import argparse
import hashlib
import json
from pathlib import Path
import plistlib
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import testflight as tf


CONTEXT = {"app_id": "123", "bundle_id": "it.example.App", "group_id": "internal"}
RECEIPT = {"schema_version": 1, **CONTEXT, "version": "1.0", "build_number": "7",
           "source_sha": "a" * 40, "ipa_sha256": None, "build_id": None, "status": "uploaded"}


def build(state="VALID", beta="IN_BETA_TESTING", app="123", number="7", expired=False):
    return {"data": {"id": "build-7", "attributes": {"version": number, "processingState": state, "expired": expired}},
            "included": [{"type": "apps", "id": app},
                         {"type": "preReleaseVersions", "attributes": {"version": "1.0"}},
                         {"type": "buildBetaDetails", "attributes": {"internalBuildState": beta}}]}


class TestFlightTests(unittest.TestCase):
    def test_wrong_app_and_external_group_rejected_before_mutation(self):
        app = {"data": {"id": "123", "attributes": {"bundleId": "it.example.App"}}}
        for internal in [False, None]:
            groups = {"data": [{"id": "internal", "attributes": {"isInternalGroup": internal}}]}
            with patch.object(tf, "command", side_effect=[("5.17.1", 0), (app, 0), (groups, 0)]) as cmd:
                with self.assertRaises(tf.Failure):
                    tf.preflight("123", "it.example.App", "internal")
                self.assertFalse(any("add-groups" in c.args[0] for c in cmd.call_args_list))
        with patch.object(tf, "command", side_effect=[("5.17.1", 0), (app, 0)]):
            with self.assertRaises(tf.Failure):
                tf.preflight("123", "wrong.bundle", "internal")

    def test_empty_internal_group_is_not_ready(self):
        responses = [("5.17.1", 0), ({"data": {"id": "123", "attributes": {"bundleId": "it.example.App"}}}, 0),
                     ({"data": [{"id": "internal", "attributes": {"isInternalGroup": True}}]}, 0), ({"data": []}, 0)]
        with patch.object(tf, "command", side_effect=responses):
            with self.assertRaises(tf.Failure):
                tf.preflight("123", "it.example.App", "internal")

    def test_ipa_bundle_and_platform_are_read_without_extraction(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "App.ipa"
            for platform in ["iPhoneSimulator", "iPhoneOS"]:
                with zipfile.ZipFile(path, "w") as archive:
                    archive.writestr("Payload/App.app/Info.plist", plistlib.dumps({
                        "CFBundleIdentifier": "it.example.App", "CFBundleShortVersionString": "1.0",
                        "CFBundleVersion": "7", "CFBundleSupportedPlatforms": [platform]}))
                if platform == "iPhoneOS":
                    self.assertEqual(tf.ipa_identity(path)["build_number"], "7")
                else:
                    with self.assertRaises(tf.Failure): tf.ipa_identity(path)

    def test_uncertain_upload_preserves_receipt_and_refuses_reupload(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            ipa = path / "App.ipa"
            ipa.write_bytes(b"fixture")
            args = argparse.Namespace(receipt=path / "receipt.json", ipa=ipa, source_sha="a" * 40,
                                      app="123", bundle_id="it.example.App", group_id="internal")
            identity = {"bundle_id": "it.example.App", "version": "1.0", "build_number": "7"}
            with patch.object(tf, "ipa_identity", return_value=identity), patch.object(tf, "preflight", return_value=CONTEXT), \
                 patch.object(tf, "command", side_effect=tf.Failure("connection lost")) as cmd:
                with self.assertRaises(tf.Failure): tf.upload(args)
                receipt = tf.load_receipt(args.receipt)
                self.assertEqual(receipt["status"], "upload_attempted")
                self.assertEqual(receipt["ipa_sha256"], hashlib.sha256(b"fixture").hexdigest())
                self.assertEqual(args.receipt.stat().st_mode & 0o777, 0o600)
                with self.assertRaises(tf.Failure): tf.upload(args)
                self.assertEqual(cmd.call_count, 1)

    def test_build_identity_and_expiry_fail_closed(self):
        for response in [build(app="another"), build(number="8"), build(expired=True),
                         build(expired=None), build(state="INVALID"), build(state="FAILED")]:
            with self.subTest(response=response):
                with self.assertRaises(tf.Failure): tf.verify_build(response, RECEIPT)

    def test_wait_timeout_is_pending_and_never_distributes(self):
        with tempfile.TemporaryDirectory() as folder:
            args = argparse.Namespace(receipt=Path(folder) / "receipt.json")
            tf.save(args.receipt, RECEIPT)
            with patch.object(tf, "preflight"), patch.object(tf, "command", return_value=({"status": "pending"}, 7)) as cmd:
                result, code = tf.follow(args, distribute=True)
            self.assertEqual(code, 7)
            self.assertEqual(cmd.call_count, 1)
            self.assertNotEqual(result["status"], "available_to_install")

    def test_status_never_adds_groups_and_requires_beta_readiness(self):
        for attached, beta, expected in [(False, "IN_BETA_TESTING", 7), (True, "MISSING_EXPORT_COMPLIANCE", 7),
                                        (True, "READY_FOR_BETA_TESTING", 7), (True, "IN_BETA_TESTING", 0)]:
            with self.subTest(attached=attached, beta=beta), tempfile.TemporaryDirectory() as folder:
                args = argparse.Namespace(receipt=Path(folder) / "receipt.json")
                tf.save(args.receipt, RECEIPT)
                with patch.object(tf, "preflight"), patch.object(tf, "membership", return_value=attached), \
                     patch.object(tf, "command", side_effect=[({}, 0), (build(beta=beta), 0)]) as cmd:
                    result, code = tf.follow(args, distribute=False)
                self.assertEqual(code, expected)
                self.assertFalse(any("add-groups" in c.args[0] for c in cmd.call_args_list))

    def test_resume_adds_only_requested_group_then_rechecks(self):
        with tempfile.TemporaryDirectory() as folder:
            args = argparse.Namespace(receipt=Path(folder) / "receipt.json")
            tf.save(args.receipt, RECEIPT)
            with patch.object(tf, "preflight"), patch.object(tf, "membership", side_effect=[False, True]), \
                 patch.object(tf, "command", side_effect=[({}, 0), (build(), 0), ({}, 0), (build(), 0)]) as cmd:
                result, code = tf.follow(args, distribute=True)
            self.assertEqual(code, 0)
            self.assertEqual(result["build_id"], "build-7")
            mutation = cmd.call_args_list[2].args[0]
            self.assertEqual(mutation, ["builds", "add-groups", "--build-id", "build-7", "--group", "internal", "--output", "json"])

    def test_partial_membership_lookup_never_proves_access(self):
        with patch.object(tf, "command", return_value=({"complete": False, "appId": "123", "buildId": "build-7",
                                                       "groups": [{"id": "internal"}]}, 0)):
            with self.assertRaises(tf.Failure): tf.membership(RECEIPT, "build-7")


if __name__ == "__main__":
    unittest.main()
