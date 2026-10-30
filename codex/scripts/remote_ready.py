#!/usr/bin/env python3
"""Bounded, read-only readiness checks. Requires Python 3.11+; no dependencies."""

import argparse
import concurrent.futures
import configparser
from dataclasses import asdict, dataclass
import json
import os
from pathlib import Path
import re
import shlex
import signal
import subprocess
import sys
import tomllib


@dataclass
class Result:
    name: str
    status: str
    detail: str
    action: str = ""


@dataclass
class Command:
    code: int
    stdout: str = ""
    stderr: str = ""
    problem: str = ""


def run(argv, timeout):
    """Never read stdin, run a shell, or show raw command output to the user."""
    env = dict(os.environ, AWS_PAGER="", GH_PAGER="cat", GH_PROMPT_DISABLED="1",
               AWS_CLI_AUTO_PROMPT="off", NO_COLOR="1")
    try:
        process = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, text=True, errors="replace",
                                   env=env, start_new_session=True)
    except FileNotFoundError:
        return Command(127, problem="missing")
    except OSError:
        return Command(126, problem="launch")
    try:
        stdout, stderr = process.communicate(timeout=timeout)
        return Command(process.returncode, stdout, stderr)
    except subprocess.TimeoutExpired:
        # Include children such as Node launchers; do not leave login jobs behind.
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.communicate()
        return Command(124, problem="timeout")


def failure(name, command, login_action, setup_action):
    message = (command.stdout + "\n" + command.stderr).lower()
    if command.problem:
        descriptions = {"missing": "Command is not installed or not on PATH.",
                        "launch": "Command could not start.",
                        "timeout": "Check timed out; no readiness result."}
        return Result(name, "setup", descriptions[command.problem], setup_action)
    if any(s in message for s in ("accessdenied", "access denied", "forbidden", "http 403", "no access")):
        return Result(name, "setup", "Access was denied; login alone may not fix the permissions.", setup_action)
    if any(s in message for s in ("sso session", "error loading sso token", "expiredtoken",
                                 "token has expired", "not logged", "authentication required",
                                 "bad credentials", "http 401", "gh auth login", "unauthorized")):
        return Result(name, "auth", "Sign-in is required or the saved session is invalid.", login_action)
    return Result(name, "setup", f"Check failed (exit {command.code}); raw output withheld.", setup_action)


def decoded(command):
    try:
        value = json.loads(command.stdout)
        return value if isinstance(value, dict) else {}
    except ValueError:
        return {}


def check_codex(timeout):
    repair = "Repair the CLI installation; then run codex --version again (see codex/SETUP.md)."
    version = run(["codex", "--version"], timeout)
    if version.code:
        return [failure("Codex CLI", version, "codex login --device-auth", repair)]
    match = re.fullmatch(r"codex-cli ([0-9][A-Za-z0-9.+-]*)\s*", version.stdout)
    if not match:
        return [Result("Codex CLI", "setup", "Unexpected CLI version response.", repair)]
    results = [Result("Codex CLI", "ready", match[1])]
    auth = run(["codex", "login", "status"], timeout)
    if auth.code:
        results.append(failure("Codex sign-in", auth, "codex login --device-auth", repair))
    else:
        results.append(Result("Codex sign-in", "ready", "Local sign-in is present; model access was not exercised."))
    return results


def check_github(timeout, repo):
    login = "gh auth login --hostname github.com --web"
    setup = "Check GitHub connectivity and the CLI account's repository permissions."
    response = run(["gh", "api", "--hostname", "github.com", "user"], timeout)
    if response.code:
        return [failure("GitHub", response, login, setup)]
    user = decoded(response).get("login")
    if not isinstance(user, str) or not re.fullmatch(r"[A-Za-z0-9_\[\]-]+", user):
        return [Result("GitHub", "setup", "The identity response was not recognised.", setup)]
    results = [Result("GitHub", "ready", f"Authenticated API read succeeded as {user}.")]
    if repo:
        response = run(["gh", "api", "--hostname", "github.com", f"repos/{repo}"], timeout)
        name = f"GitHub {repo}"
        if response.code:
            results.append(failure(name, response, login, setup))
        else:
            data = decoded(response)
            full_name = data.get("full_name")
            permissions = data.get("permissions")
            if not isinstance(full_name, str) or full_name.lower() != repo.lower():
                results.append(Result(name, "setup", "Repository identity did not match.", setup))
            elif not isinstance(permissions, dict) or permissions.get("push") is not True:
                results.append(Result(name, "setup", "Read succeeded; push permission was not confirmed.", setup))
            else:
                results.append(Result(name, "ready", "Read succeeded; GitHub reports push permission. PR creation and branch rules were not tested."))
    return results


def aws_target(profile):
    config = configparser.RawConfigParser()
    with Path(os.environ.get("AWS_CONFIG_FILE", str(Path.home() / ".aws/config"))).expanduser().open() as file:
        config.read_file(file)
    name = "default" if profile == "default" else f"profile {profile}"
    if not config.has_section(name):
        return None
    selected = config[name]
    if selected.get("sso_account_id") and selected.get("sso_role_name"):
        return selected["sso_account_id"], selected["sso_role_name"], True
    role = re.fullmatch(r"arn:[^:]+:iam::([0-9]{12}):role/(.+)", selected.get("role_arn", ""))
    if role:
        return role[1], role[2].split("/")[-1], False
    return None


def check_aws(timeout, profile):
    name = f"AWS {profile}"
    login = f"aws sso login --profile {shlex.quote(profile)} --use-device-code --no-browser"
    setup = "Check the selected profile, expected account/role, network, and AWS permissions."
    try:
        target = aws_target(profile)
    except (OSError, configparser.Error):
        return [Result(name, "setup", "AWS profile configuration could not be read.", setup)]
    if not target:
        return [Result(name, "setup", "Profile needs an expected SSO account/role or role_arn for identity verification.", setup)]
    response = run(["aws", "sts", "get-caller-identity", "--profile", profile, "--output", "json",
                    "--no-cli-pager", "--cli-connect-timeout", str(timeout), "--cli-read-timeout", str(timeout)], timeout)
    if response.code:
        return [failure(name, response, login, setup)]
    identity = decoded(response)
    arn = identity.get("Arn")
    role = re.fullmatch(r"arn:[^:]+:sts::([0-9]{12}):assumed-role/([^/]+)/.+", arn) if isinstance(arn, str) else None
    account, expected_role, sso = target
    expected = rf"AWSReservedSSO_{re.escape(expected_role)}_[0-9a-f]+" if sso else re.escape(expected_role)
    if not role or identity.get("Account") != account or role[1] != account or not re.fullmatch(expected, role[2]):
        return [Result(name, "setup", "AWS returned an unexpected account or role; do not continue.", setup)]
    return [Result(name, "ready", f"Account and role match the profile ({expected_role}). Service read/write access was not tested.")]


def check_xcode(timeout):
    setup = "Check xcode-select, Xcode first-launch setup, and installed iOS simulator runtimes."
    build = run(["xcodebuild", "-version"], timeout)
    if build.code:
        return [failure("Xcode", build, setup, setup)]
    match = re.search(r"^Xcode ([0-9.]+)", build.stdout)
    if not match:
        return [Result("Xcode", "setup", "Full Xcode was not confirmed.", setup)]
    results = [Result("Xcode", "ready", f"Xcode {match[1]}; signing and UI control were not tested.")]
    response = run(["xcrun", "simctl", "list", "devices", "available", "--json"], timeout)
    if response.code:
        results.append(failure("iOS simulator", response, setup, setup))
    else:
        runtimes = decoded(response).get("devices")
        if not isinstance(runtimes, dict):
            return results + [Result("iOS simulator", "setup", "Simulator response was not recognised.", setup)]
        devices = [d for runtime, entries in runtimes.items()
                   if ".iOS-" in runtime and isinstance(entries, list)
                   for d in entries if isinstance(d, dict) and d.get("isAvailable") is True]
        if devices:
            booted = sum(d.get("state") == "Booted" for d in devices)
            results.append(Result("iOS simulator", "ready", f"{len(devices)} available devices; {booted} booted. No device was started."))
        else:
            results.append(Result("iOS simulator", "setup", "No available iOS simulator device was found.", setup))
    return results


def check_mcp(names):
    """Configuration is not a live connection. The agent must perform the read."""
    path = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "config.toml"
    try:
        with path.open("rb") as file:
            servers = tomllib.load(file).get("mcp_servers", {})
    except (OSError, ValueError):
        servers = {}
    if not isinstance(servers, dict):
        servers = {}
    results = []
    for name in names:
        server = servers.get(name)
        if isinstance(server, dict) and server.get("enabled", True):
            detail = "Enabled in local config; authentication and live access are unverified."
        elif isinstance(server, dict):
            detail = "Disabled in local config; a separate connected plugin may still be available."
        else:
            detail = "No global local-MCP entry; a connected plugin or project configuration may still provide it."
        results.append(Result(f"MCP {name}", "verify", detail,
                              "In this Codex chat, discover the service's tool and perform a harmless authenticated read."))
    return results


def report(results):
    return {"schema_version": 1, "ready": all(r.status == "ready" for r in results),
            "checks": [asdict(r) for r in results],
            "scope": "Only requested checks. No login, writes, builds, or model requests. Browser/MCP reads require the current agent session."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", help="Optional GitHub owner/repo to check")
    parser.add_argument("--aws-profile", help="Optional AWS profile; verifies its configured account and role")
    parser.add_argument("--xcode", action="store_true", help="Check Xcode and available iOS simulator devices")
    parser.add_argument("--mcp", action="append", default=[], metavar="NAME", help="Report MCP configuration and require an agent read; repeatable")
    parser.add_argument("--browser", action="store_true", help="Require a browser-control check in the current agent session")
    parser.add_argument("--json", action="store_true", help="Emit a structured report, including unverified capabilities")
    parser.add_argument("--timeout", type=int, default=10, help="Per-command deadline in seconds (1–30; default 10)")
    args = parser.parse_args()
    if not 1 <= args.timeout <= 30:
        parser.error("--timeout must be between 1 and 30")
    if args.repo and not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", args.repo):
        parser.error("--repo must be owner/repo")
    for value in [args.aws_profile, *args.mcp]:
        if value and (len(value) > 128 or not re.fullmatch(r"[A-Za-z0-9_.@+ -]+", value) or value.startswith("-")):
            parser.error("profile and server names must be plain names of at most 128 characters")
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        jobs = [pool.submit(check_codex, args.timeout), pool.submit(check_github, args.timeout, args.repo)]
        if args.aws_profile:
            jobs.append(pool.submit(check_aws, args.timeout, args.aws_profile))
        if args.xcode:
            jobs.append(pool.submit(check_xcode, args.timeout))
        results = [result for job in jobs for result in job.result()]
    results.extend(check_mcp(list(dict.fromkeys(args.mcp))))
    if args.browser:
        results.append(Result("Browser control", "verify", "A shell process cannot prove this chat can control the browser.",
                              "Use the current browser tool to list tabs and read one task-relevant page without navigating or changing it."))
    data = report(results)
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        labels = {"ready": "READY", "auth": "SIGN IN", "setup": "ATTENTION", "verify": "VERIFY"}
        for result in results:
            print(f"{labels[result.status]:9} {result.name}: {result.detail}")
            if result.action:
                print(f"          Next: {result.action}")
        print("\n" + data["scope"])
    return 0 if data["ready"] else 1


if __name__ == "__main__":
    sys.exit(main())
