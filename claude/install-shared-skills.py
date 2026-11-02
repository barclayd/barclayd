#!/usr/bin/env python3
"""Link this repository's shared skills and the installed ASC pack into Claude Code."""

import argparse
from pathlib import Path
import sys


SHARED_SKILLS = (
    "apple-app-architecture", "aws-sso-login", "remote-ready", "remote-handoff", "simulator-control",
    "testflight-release",
)
COMMANDS = {
    "testflight": "codex/scripts/testflight.py",
    "remote-ready": "codex/scripts/remote_ready.py",
    "duoctl": "codex/skills/simulator-control/vendor/duoctl/duoctl",
}
REQUIRED_ASC = {"asc-cli-usage", "asc-signing-setup", "asc-xcode-build", "asc-testflight-orchestration"}


def planned_links(repo, skills_dir, bin_dir, asc_dir):
    upstream = sorted(asc_dir.glob("asc-*/SKILL.md"))
    if not REQUIRED_ASC.issubset({path.parent.name for path in upstream}):
        raise ValueError("ASC skills are missing. Run asc install-skills first.")
    sources = [repo / "codex" / "skills" / name for name in SHARED_SKILLS]
    sources += [path.parent for path in upstream]
    for source in sources:
        if not (source / "SKILL.md").is_file():
            raise ValueError(f"Missing skill: {source}")
    links = [(source, skills_dir / source.name) for source in sources]
    for name, script in COMMANDS.items():
        source = repo / script
        if not source.is_file():
            raise ValueError(f"Missing command: {source}")
        links.append((source, bin_dir / name))
    return links


def install_links(links):
    # Check every destination before creating any links; preserve other installations.
    for source, destination in links:
        if destination.is_symlink() and destination.resolve() == source.resolve():
            continue
        if destination.exists() or destination.is_symlink():
            raise ValueError(f"Destination already exists; leaving it untouched: {destination}")
    for source, destination in links:
        destination.parent.mkdir(parents=True, exist_ok=True)
        if not destination.is_symlink():
            destination.symlink_to(source, target_is_directory=source.is_dir())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-dir", type=Path, default=Path.home() / ".claude/skills")
    parser.add_argument("--bin-dir", type=Path, default=Path.home() / ".local/bin")
    parser.add_argument("--asc-skills-dir", type=Path, default=Path.home() / ".agents/skills")
    args = parser.parse_args()
    if sys.version_info < (3, 11):
        parser.exit(1, "Python 3.11+ is required by the shared commands.\n")
    repo = Path(__file__).resolve().parents[1]
    try:
        links = planned_links(repo, args.skills_dir.expanduser().absolute(),
                              args.bin_dir.expanduser().absolute(), args.asc_skills_dir.expanduser().absolute())
        install_links(links)
    except (ValueError, OSError) as error:
        parser.exit(1, f"{error}\n")
    print(f"Installed {len(links) - len(COMMANDS)} skills and {len(COMMANDS)} command links for Claude Code.")
    print("Open a fresh Claude Code session and use /testflight-release.")


if __name__ == "__main__":
    main()
