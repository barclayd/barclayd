import contextlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest.mock import mock_open, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import remote_ready as rr


class ReadinessTests(unittest.TestCase):
    def test_broken_codex_does_not_use_desktop_fallback_to_claim_ready(self):
        broken = rr.Command(1, stderr="spawn ENOENT Authorization: Bearer secret-value")
        with patch.object(rr, "run", return_value=broken) as command:
            results = rr.check_codex(2)
        self.assertEqual(command.call_count, 1)
        self.assertEqual(results[0].status, "setup")
        self.assertNotIn("secret-value", json.dumps(rr.report(results)))

    def test_local_auth_output_is_not_echoed(self):
        with patch.object(rr, "run", side_effect=[rr.Command(0, "codex-cli 0.166.0\n"),
                                                  rr.Command(0, stderr="Logged in using API key: secret-value")]):
            results = rr.check_codex(2)
        self.assertTrue(rr.report(results)["ready"])
        self.assertNotIn("secret-value", json.dumps(rr.report(results)))
        self.assertIn("not exercised", results[1].detail)

    def test_github_read_access_does_not_imply_push_access(self):
        with patch.object(rr, "run", side_effect=[rr.Command(0, '{"login":"example"}'),
                                                  rr.Command(0, '{"full_name":"example/repo","permissions":{"push":false}}')]):
            results = rr.check_github(2, "example/repo")
        self.assertEqual([r.status for r in results], ["ready", "setup"])

    def aws_check(self, response, account="123456789012", role="ViewOnlyAccess"):
        with patch.object(rr, "aws_target", return_value=(account, role, True)), patch.object(rr, "run", return_value=response):
            return rr.check_aws(2, "production")[0]

    def test_aws_verifies_both_account_and_role(self):
        for account, role, expected in [
            ("123456789012", "AWSReservedSSO_ViewOnlyAccess_abcdef123456", "ready"),
            ("999999999999", "AWSReservedSSO_ViewOnlyAccess_abcdef123456", "setup"),
            ("123456789012", "AWSReservedSSO_AdministratorAccess_abcdef123456", "setup"),
        ]:
            with self.subTest(account=account, role=role):
                response = rr.Command(0, json.dumps({"Account":account, "Arn":f"arn:aws:sts::{account}:assumed-role/{role}/example"}))
                self.assertEqual(self.aws_check(response).status, expected)

    def test_sts_arn_account_must_also_match(self):
        response = rr.Command(0, json.dumps({"Account":"123456789012", "Arn":"arn:aws:sts::999999999999:assumed-role/AWSReservedSSO_ViewOnlyAccess_abcdef/example"}))
        self.assertEqual(self.aws_check(response).status, "setup")

    def test_sso_expiry_uses_phone_flow_but_permission_denial_does_not(self):
        expired = self.aws_check(rr.Command(255, stderr="The SSO session associated with this profile has expired"))
        self.assertEqual(expired.status, "auth")
        self.assertEqual(expired.action, "aws sso login --profile production --use-device-code --no-browser")
        denied = self.aws_check(rr.Command(255, stderr="AccessDeniedException: SSO session has no access"))
        self.assertEqual(denied.status, "setup")
        self.assertNotIn("sso login", denied.action)

    def test_malformed_identity_does_not_pass(self):
        self.assertEqual(self.aws_check(rr.Command(0, "not-json")).status, "setup")
        self.assertEqual(self.aws_check(rr.Command(0, "[]")).status, "setup")
        self.assertEqual(self.aws_check(rr.Command(0, '{"Arn":null}')).status, "setup")

    def test_malformed_repository_and_simulator_responses_do_not_crash(self):
        with patch.object(rr, "run", side_effect=[rr.Command(0, '{"login":"example"}'),
                                                  rr.Command(0, '{"full_name":"example/repo","permissions":null}')]):
            self.assertEqual(rr.check_github(2, "example/repo")[-1].status, "setup")
        with patch.object(rr, "run", side_effect=[rr.Command(0, 'Xcode 27.1'),
                                                  rr.Command(0, '{"devices":null}')]):
            self.assertEqual(rr.check_xcode(2)[-1].status, "setup")

    def test_reads_selected_profile_without_reading_credentials(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config"
            path.write_text("[profile production]\nsso_account_id = 123456789012\nsso_role_name = ViewOnlyAccess\n[profile another]\nrole_arn = arn:aws:iam::999999999999:role/team/Deploy\n")
            with patch.dict(os.environ, {"AWS_CONFIG_FILE":str(path)}):
                self.assertEqual(rr.aws_target("production"), ("123456789012", "ViewOnlyAccess", True))
                self.assertEqual(rr.aws_target("another"), ("999999999999", "Deploy", False))
                self.assertIsNone(rr.aws_target("absent"))

    def test_mcp_config_never_proves_access_or_exposes_secrets(self):
        config = b'[mcp_servers.sentry]\nurl = "https://example.com"\n[mcp_servers.sentry.http_headers]\nAuthorization = "Bearer secret-value"\n'
        with patch.object(Path, "open", mock_open(read_data=config)):
            results = rr.check_mcp(["sentry", "missing"])
        self.assertEqual([r.status for r in results], ["verify", "verify"])
        self.assertFalse(rr.report(results)["ready"])
        self.assertNotIn("secret-value", json.dumps(rr.report(results)))

    def test_network_failure_is_not_a_login_request(self):
        result = self.aws_check(rr.Command(255, stderr="Could not connect to the endpoint URL"))
        self.assertEqual(result.status, "setup")
        self.assertNotIn("sso login", result.action)

    def test_timeout_kills_child_processes(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "child-completed"
            child = "import time; from pathlib import Path; time.sleep(0.5); Path(" + repr(str(marker)) + ").touch()"
            parent = "import subprocess,sys,time; subprocess.Popen([sys.executable,'-c'," + repr(child) + "]); time.sleep(20)"
            result = rr.run([sys.executable, "-c", parent], 0.15)
            self.assertEqual(result.problem, "timeout")
            time.sleep(0.6)
            self.assertFalse(marker.exists(), "The timed-out check left a child running")

    def test_command_cannot_wait_for_user_input(self):
        result = rr.run([sys.executable, "-c", "import sys; print(repr(sys.stdin.read()))"], 1)
        self.assertEqual(result.code, 0)
        self.assertEqual(result.stdout.strip(), "''")

    def test_json_exit_code_includes_pending_agent_probes(self):
        output = io.StringIO()
        ready = [rr.Result("fixture", "ready", "passed")]
        with patch.object(sys, "argv", ["remote-ready", "--browser", "--json"]), \
                patch.object(rr, "check_codex", return_value=ready), \
                patch.object(rr, "check_github", return_value=ready), contextlib.redirect_stdout(output):
            code = rr.main()
        data = json.loads(output.getvalue())
        self.assertEqual(code, 1)
        self.assertFalse(data["ready"])
        self.assertEqual(data["checks"][-1]["status"], "verify")


if __name__ == "__main__":
    unittest.main()
