#!/usr/bin/env python3
"""Upload an existing iOS IPA and resume internal TestFlight delivery. Python 3.11+."""

import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import plistlib
import re
import signal
import subprocess
import sys
import tempfile
import time
import zipfile


ASC_VERSION = "5.17.1"


class Failure(Exception):
    pass


def command(args, *, timeout=60, log=None, pending=False, attempt=0):
    """No shell, stdin or raw diagnostic output. Retain private logs when requested."""
    env = dict(os.environ, ASC_TELEMETRY_DISABLED="1", NO_COLOR="1",
               ASC_TIMEOUT="45s", ASC_UPLOAD_TIMEOUT="25m")
    try:
        profile = os.environ.get("TESTFLIGHT_ASC_PROFILE")
        argv = ["asc", *(["--profile", profile] if profile else []), *args]
        process = subprocess.Popen(argv, stdin=subprocess.DEVNULL,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   text=True, env=env, start_new_session=True)
    except OSError as error:
        raise Failure("ASC could not start; install it and check PATH.") from error
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except (subprocess.TimeoutExpired, KeyboardInterrupt):
        os.killpg(process.pid, signal.SIGTERM)
        try:
            stdout, stderr = process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            stdout, stderr = process.communicate()
        if log:
            private_write(log, stdout + "\n" + stderr)
        raise Failure("ASC interrupted or timed out. Resume the receipt; do not repeat an upload.")
    if log:
        private_write(log, stdout + "\n" + stderr)
    if process.returncode and not (pending and process.returncode == 7):
        read_only = any(args[:len(prefix)] == prefix for prefix in [
            ["apps", "view"], ["testflight", "groups", "list"],
            ["testflight", "groups", "testers", "list"], ["builds", "info"]])
        transient = re.search(r"(?i)(timed? out|timeout|connection reset|connection refused|temporary|tls handshake|\b429\b|\b50[234]\b)", stderr)
        if read_only and transient and attempt < 2:
            time.sleep(attempt + 1)
            return command(args, timeout=timeout, log=log, pending=pending, attempt=attempt + 1)
        suffix = f" Inspect private log {log}." if log else " Check ASC auth and command permissions."
        raise Failure(f"ASC {' '.join(args[:2])} failed (exit {process.returncode})." + suffix)
    if args == ["version"]:
        return stdout.strip(), 0
    try:
        data = json.loads(stdout)
        if not isinstance(data, dict):
            raise ValueError()
    except ValueError as error:
        raise Failure("ASC returned an unexpected response; no success was inferred.") from error
    return data, process.returncode


def private_write(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, temp = tempfile.mkstemp(prefix=".testflight-", dir=path.parent)
    try:
        with os.fdopen(fd, "w") as file:
            file.write(text)
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def save(path, receipt):
    private_write(path, json.dumps(receipt, indent=2) + "\n")


def preflight(app, bundle, group):
    version, _ = command(["version"])
    if version.split()[0] != ASC_VERSION:
        raise Failure(f"Use tested ASC {ASC_VERSION}; found {version.split()[0]}.")
    result, _ = command(["apps", "view", "--id", app, "--fields", "name,bundleId", "--output", "json"])
    data = result.get("data", {})
    if data.get("id") != app or data.get("attributes", {}).get("bundleId") != bundle:
        raise Failure("App ID and bundle ID do not match the authenticated Apple account.")
    groups, _ = command(["testflight", "groups", "list", "--app", app, "--paginate", "--output", "json"])
    matches = [g for g in groups.get("data", []) if g.get("id") == group]
    if len(matches) != 1 or matches[0].get("attributes", {}).get("isInternalGroup") is not True:
        raise Failure("The selected group is not an internal group belonging to this app.")
    testers, _ = command(["testflight", "groups", "testers", "list", "--group-id", group,
                          "--fields", "state", "--paginate", "--output", "json"])
    if not testers.get("data"):
        raise Failure("The internal group has no testers; configure the intended tester first.")
    return {"app_id": app, "bundle_id": bundle, "group_id": group,
            "group_name": matches[0]["attributes"].get("name"), "tester_count": len(testers["data"])}


def ipa_identity(path):
    try:
        with zipfile.ZipFile(path) as archive:
            names = [n for n in archive.namelist() if re.fullmatch(r"Payload/[^/]+\.app/Info\.plist", n)]
            if len(names) != 1:
                raise Failure("IPA must contain exactly one top-level iOS app.")
            info = plistlib.loads(archive.read(names[0]))
    except (OSError, ValueError, zipfile.BadZipFile, plistlib.InvalidFileException) as error:
        raise Failure("Cannot read the IPA's app Info.plist.") from error
    fields = [info.get(k) for k in ("CFBundleIdentifier", "CFBundleShortVersionString", "CFBundleVersion")]
    if not all(isinstance(v, str) and v.strip() for v in fields):
        raise Failure("IPA is missing its bundle ID, marketing version or build number.")
    if "iPhoneOS" not in info.get("CFBundleSupportedPlatforms", []):
        raise Failure("Expected an iPhoneOS IPA, not a simulator or another platform.")
    return dict(zip(("bundle_id", "version", "build_number"), fields))


def upload(args):
    path = args.receipt.resolve()
    if path.exists():
        raise Failure("Receipt already exists. Use resume; a second upload was not attempted.")
    if not re.fullmatch(r"[0-9a-f]{40}", args.source_sha):
        raise Failure("Supply the full 40-character source SHA actually used to build this IPA.")
    identity = ipa_identity(args.ipa)
    if identity["bundle_id"] != args.bundle_id:
        raise Failure("IPA bundle ID does not match the requested app.")
    context = preflight(args.app, args.bundle_id, args.group_id)
    with args.ipa.open("rb") as file:
        digest = hashlib.file_digest(file, "sha256").hexdigest()
    receipt = {"schema_version": 1, **context, **identity, "source_sha": args.source_sha,
               "ipa_sha256": digest, "status": "upload_attempted", "build_id": None}
    # Written before the network mutation: an ambiguous failure is recoverable.
    save(path, receipt)
    result, _ = command(["builds", "upload", "--app", args.app, "--ipa", str(args.ipa.resolve()),
                         "--output", "json"], timeout=1800, log=path.with_suffix(".upload.log"))
    receipt["build_id"] = result.get("buildId")
    receipt["status"] = "uploaded"
    save(path, receipt)
    return receipt, 0


def load_receipt(path):
    try:
        receipt = json.loads(path.read_text())
        required = ("app_id", "bundle_id", "group_id", "version", "build_number", "source_sha")
        if receipt.get("schema_version") != 1 or not all(isinstance(receipt[k], str) and receipt[k] for k in required):
            raise ValueError()
        return receipt
    except (OSError, ValueError, KeyError, AttributeError) as error:
        raise Failure("Receipt is missing or invalid; no Apple mutation was attempted.") from error


def selector(receipt):
    return ["--app", receipt["app_id"], "--build-number", receipt["build_number"],
            "--version", receipt["version"], "--platform", "IOS"]


def track(args):
    if args.receipt.exists():
        raise Failure("Receipt already exists; use status or resume.")
    if not re.fullmatch(r"[0-9a-f]{40}", args.source_sha):
        raise Failure("Supply the full source SHA actually archived.")
    receipt = {"schema_version": 1, **preflight(args.app, args.bundle_id, args.group_id),
               "version": args.version, "build_number": args.build_number,
               "source_sha": args.source_sha, "ipa_sha256": None, "build_id": None,
               "status": "existing_upload_unverified"}
    save(args.receipt, receipt)
    return follow(args, distribute=False)


def verify_build(result, receipt):
    build = result.get("data", {})
    attributes = build.get("attributes", {})
    included = result.get("included", [])
    apps = [r for r in included if r.get("type") == "apps"]
    versions = [r for r in included if r.get("type") == "preReleaseVersions"]
    if (not build.get("id") or attributes.get("version") != receipt["build_number"]
            or not any(a.get("id") == receipt["app_id"] for a in apps)
            or not any(v.get("attributes", {}).get("version") == receipt["version"] for v in versions)):
        raise Failure("Apple build identity does not match the receipt; distribution stopped.")
    if receipt.get("build_id") and receipt["build_id"] != build["id"]:
        raise Failure("Apple returned a different build ID from the saved receipt.")
    if attributes.get("expired") is not False:
        raise Failure("Build is expired or its expiry status was not returned.")
    state = attributes.get("processingState")
    if state in ("FAILED", "INVALID"):
        raise Failure(f"Apple build processing is {state}; inspect the exact build before retrying.")
    beta = [r for r in included if r.get("type") == "buildBetaDetails"]
    return build["id"], state, beta[0].get("attributes", {}).get("internalBuildState") if len(beta) == 1 else None


def membership(receipt, build_id):
    result, _ = command(["testflight", "groups", "list", "--build-id", build_id,
                         "--app", receipt["app_id"], "--internal", "--output", "json"])
    if result.get("complete") is not True or result.get("buildId") != build_id or result.get("appId") != receipt["app_id"]:
        raise Failure("Apple group membership lookup was incomplete or mismatched.")
    return any(g.get("id") == receipt["group_id"] for g in result.get("groups", []))


def follow(args, distribute):
    receipt = load_receipt(args.receipt)
    preflight(receipt["app_id"], receipt["bundle_id"], receipt["group_id"])
    _, code = command(["builds", "wait", *selector(receipt), "--timeout", "45s",
                       "--poll-interval", "10s", "--report-pending", "--fail-on-invalid", "--output", "json"],
                      timeout=55, pending=True, log=args.receipt.with_suffix(".processing.log"))
    if code == 7:
        receipt["status"] = "processing_or_discovery_pending"
        save(args.receipt, receipt)
        return receipt, 7
    info_args = ["builds", "info", *selector(receipt), "--include", "app,preReleaseVersion,buildBetaDetail", "--output", "json"]
    info, _ = command(info_args)
    build_id, state, beta_state = verify_build(info, receipt)
    receipt["build_id"] = build_id
    save(args.receipt, receipt)
    attached = membership(receipt, build_id)
    if state == "VALID" and not attached and distribute:
        command(["builds", "add-groups", "--build-id", build_id, "--group", receipt["group_id"], "--output", "json"],
                log=args.receipt.with_suffix(".distribution.log"))
        attached = membership(receipt, build_id)
        info, _ = command(info_args)
        build_id, state, beta_state = verify_build(info, receipt)
    ready = state == "VALID" and attached and beta_state == "IN_BETA_TESTING"
    receipt.update(status="available_to_install" if ready else "availability_pending",
                   processing_state=state, internal_build_state=beta_state, group_access=attached)
    save(args.receipt, receipt)
    return receipt, 0 if ready else 7


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="action", required=True)
    for name in ("check", "upload", "track"):
        command_parser = sub.add_parser(name)
        command_parser.add_argument("--app", required=True)
        command_parser.add_argument("--bundle-id", required=True)
        command_parser.add_argument("--group-id", required=True)
        if name != "check":
            command_parser.add_argument("--source-sha", required=True)
            command_parser.add_argument("--receipt", required=True, type=Path)
        if name == "upload":
            command_parser.add_argument("--ipa", required=True, type=Path)
        if name == "track":
            command_parser.add_argument("--version", required=True)
            command_parser.add_argument("--build-number", required=True)
    for name in ("resume", "status"):
        sub.add_parser(name).add_argument("--receipt", required=True, type=Path)
    return p


def main():
    args = parser().parse_args()
    os.umask(0o077)
    try:
        # A shared host lock serialises this helper across checkouts. CI needs its
        # own concurrency group; this is not a cross-machine build reservation.
        lock_dir = Path.home() / ".local/state/testflight"
        lock_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
        app = args.app if args.action in ("check", "upload", "track") else load_receipt(args.receipt)["app_id"]
        with (lock_dir / (hashlib.sha256(app.encode()).hexdigest() + ".lock")).open("a") as lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as error:
                raise Failure("Another TestFlight helper is running for this app; wait for it to finish.") from error
            if args.action == "check":
                result, code = {"status": "api_access_verified", **preflight(args.app, args.bundle_id, args.group_id),
                                "signing_verified": False}, 0
            elif args.action == "upload":
                result, code = upload(args)
            elif args.action == "track":
                result, code = track(args)
            else:
                result, code = follow(args, distribute=args.action == "resume")
        print(json.dumps(result, indent=2))
        return code
    except (Failure, OSError) as error:
        print(json.dumps({"status": "blocked", "detail": str(error)}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
