#!/usr/bin/env python3
"""Prepare/clean one iOS target's manual signing on a dedicated macOS CI runner."""
import argparse
import base64
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import plistlib
import secrets
import shutil
import subprocess


def run(args):
    result = subprocess.run(args, capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=90)
    if result.returncode:
        raise RuntimeError(f"Signing command {args[0]} {args[1]} failed (exit {result.returncode}); output withheld.")
    return result.stdout


def profile_identity(data, bundle, team):
    entitlements = data.get("Entitlements", {})
    expiration = data["ExpirationDate"].replace(tzinfo=timezone.utc)
    if (data.get("TeamIdentifier") != [team] or entitlements.get("application-identifier") != f"{team}.{bundle}"
            or entitlements.get("get-task-allow") is not False or data.get("ProvisionedDevices")
            or data.get("ProvisionsAllDevices") or expiration <= datetime.now(timezone.utc)):
        raise ValueError("Profile is not a current App Store profile for the requested app/team.")
    return data["UUID"]


def prepare(folder):
    folder.mkdir(mode=0o700, parents=True, exist_ok=False)
    # Created first, so cleanup also works after a partial setup failure.
    state = {"profile_created": False, "profile_path": None}
    (folder / "state.json").write_text(json.dumps(state))
    for name, filename in [("DISTRIBUTION_P12_B64", "identity.p12"), ("APP_STORE_PROFILE_B64", "App.mobileprovision")]:
        value = os.environ.get(name)
        if not value:
            raise ValueError(f"Missing {name} in the caller's testflight environment secrets.")
        (folder / filename).write_bytes(base64.b64decode(value, validate=True))
    password = os.environ.get("DISTRIBUTION_P12_PASSWORD")
    if not password:
        raise ValueError("Missing DISTRIBUTION_P12_PASSWORD.")
    (folder / "identity-password").write_text(password)
    (folder / "keychain-password").write_text(secrets.token_urlsafe(32))
    profile = plistlib.loads(run(["security", "cms", "-D", "-i", str(folder / "App.mobileprovision")]).encode())
    uuid = profile_identity(profile, os.environ["BUNDLE_ID"], os.environ["TEAM_ID"])
    if not isinstance(uuid, str) or not all(c in "0123456789abcdefABCDEF-" for c in uuid) or len(uuid) != 36:
        raise ValueError("Invalid profile UUID.")
    target = Path.home() / "Library/Developer/Xcode/UserData/Provisioning Profiles" / f"{uuid}.mobileprovision"
    state["profile_path"] = str(target)
    if target.exists():
        if target.read_bytes() != (folder / "App.mobileprovision").read_bytes():
            raise ValueError("A different profile already exists at the target path; left unchanged.")
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        # Record ownership before creating the file, for partial-failure cleanup.
        state["profile_created"] = True
        (folder / "state.json").write_text(json.dumps(state))
        with target.open("xb") as file:
            file.write((folder / "App.mobileprovision").read_bytes())
    (folder / "state.json").write_text(json.dumps(state))
    result = json.loads(run(["asc", "signing", "keychain", "install", "--identity", str(folder / "identity.p12"),
        "--identity-password-file", str(folder / "identity-password"), "--keychain", str(folder / "signing.keychain-db"),
        "--keychain-password-file", str(folder / "keychain-password"), "--add-to-search-list", "--confirm", "--output", "json"]))
    if result.get("teamId") != os.environ["TEAM_ID"]:
        raise ValueError("Signing certificate belongs to a different team.")
    options = {"method": "app-store-connect", "destination": "export", "teamID": os.environ["TEAM_ID"],
               "signingStyle": "manual", "signingCertificate": result["certificateSha1"],
               "provisioningProfiles": {os.environ["BUNDLE_ID"]: uuid},
               "testFlightInternalTestingOnly": True, "manageAppVersionAndBuildNumber": False,
               "uploadSymbols": True}
    (folder / "ExportOptions.plist").write_bytes(plistlib.dumps(options))
    with open(os.environ["GITHUB_ENV"], "a") as file:
        file.write(f"SIGNING_DIR={folder}\nPROFILE_UUID={uuid}\n")
    print("Temporary signing prepared for the requested app and team.")


def cleanup(folder):
    if not folder.exists():
        return
    keychain = folder / "signing.keychain-db"
    if keychain.exists():
        run(["asc", "signing", "keychain", "delete", "--keychain", str(keychain), "--confirm", "--output", "json"])
    state_path = folder / "state.json"
    if state_path.exists():
        state = json.loads(state_path.read_text())
        if state.get("profile_created") and state.get("profile_path"):
            target = Path(state["profile_path"])
            if target.exists() and target.read_bytes() == (folder / "App.mobileprovision").read_bytes():
                target.unlink()
    shutil.rmtree(folder)
    print("Temporary signing removed.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["prepare", "cleanup"])
    args = parser.parse_args()
    os.umask(0o077)
    if os.environ.get("CI") != "true" or not os.environ.get("RUNNER_TEMP"):
        parser.error("Run only in a dedicated CI runner with CI=true and RUNNER_TEMP set.")
    folder = Path(os.environ["RUNNER_TEMP"]) / "testflight-signing"
    try:
        (prepare if args.action == "prepare" else cleanup)(folder)
    except (ValueError, KeyError, RuntimeError, OSError, subprocess.TimeoutExpired) as error:
        raise SystemExit(f"Signing {args.action} failed: {error}") from None


if __name__ == "__main__":
    main()
