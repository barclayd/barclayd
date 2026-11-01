# Claude Code Setup

## Shared architecture, delivery and access skills

From this checkout, install the ASC pack and link the shared skills into Claude:

```sh
brew install asc
asc install-skills
python3 claude/install-shared-skills.py
```

This links `apple-app-architecture`, `testflight-release`, `remote-handoff`,
`remote-ready` and `aws-sso-login` from `codex/skills`, plus the installed `asc-*` pack from
`~/.agents/skills`, into `~/.claude/skills`. The files are shared with Codex, so
edits stay in sync. It also links `testflight` and `remote-ready` into
`~/.local/bin`; ensure that directory is on PATH. Python 3.11+ is required.

The installer is safe to rerun and refuses conflicting files or symlinks before
creating any links. Use `--skills-dir`, `--bin-dir` or `--asc-skills-dir` for
custom locations. It doesn't download or update skills itself; `asc install-skills`
uses the reviewed upstream pack pinned by ASC. Keep both source directories
available. See [the shared setup](../codex/SETUP.md) for CLI and signing details.

Open a fresh Claude Code session and invoke `/apple-app-architecture`,
`/testflight-release`, `/remote-handoff`, `/remote-ready` or `/aws-sso-login`. Existing ASC credentials
and signing assets work under the same macOS user; this installer doesn't copy
credentials or change Claude's permissions. `remote-ready` still reports Codex
CLI/sign-in checks explicitly; those don't establish Claude authentication.

These are local Claude Code skills, not an upload to Claude.ai or Cowork.
Claude supports personal skills and symlinked skill folders in its
[skills documentation](https://code.claude.com/docs/en/skills).

For the architecture skill alone, no ASC setup is needed. From this checkout,
link `codex/skills/apple-app-architecture` into `~/.claude/skills/` using the
absolute source path, preserving any existing installation. It uses the same
new-app and migration guides as Codex.

## Skills

Symlink each skill into `~/.claude/skills` so Claude Code picks it up across every project:

```shell
mkdir -p ~/.claude/skills
ln -s ~/<PATH_TO_THIS_REPO>/claude/skills/pr-and-commit-style ~/.claude/skills/pr-and-commit-style
ln -s ~/<PATH_TO_THIS_REPO>/claude/skills/iphone-duo-design ~/.claude/skills/iphone-duo-design
```

* `pr-and-commit-style` => commit messages, branch names, PR titles and PR descriptions in my style (distilled from my PRs and commits before AI started writing them)
* `iphone-duo-design` => designing and adapting iOS apps for iPhone Duo (the rail, side-by-side panes, tent mode, reserved regions, mock-ups and SwiftUI pitfalls), from Apple's HIG, docs and tech talks plus lessons from building on a real device
