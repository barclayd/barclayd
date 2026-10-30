# Codex setup

## Remote readiness

From this repository, install the command and global skill:

```sh
./codex/install-remote-ready.sh
```

Requires Python 3.11+ and `~/.local/bin` on PATH. The installer creates symlinks
into this checkout and refuses to replace existing files. Keep the checkout
available. `REMOTE_READY_BIN_DIR` can select another command directory; the skill
uses `$CODEX_HOME/skills` or `~/.codex/skills`.

```sh
remote-ready
remote-ready --repo barclayd/barclayd --aws-profile production
remote-ready --xcode --browser --mcp sentry --mcp lambdatest --json
```

The default checks the terminal Codex installation, local sign-in, and a GitHub
API identity read. Optional checks cover repository permissions, the selected AWS
account/role, Xcode, and iOS simulator availability. Commands run concurrently with
a 10-second deadline per command (`--timeout` accepts 1–30 seconds).

`READY` means the stated check passed. `SIGN IN` means credentials need attention.
`ATTENTION` covers missing tools, denied access, identity mismatches, or failures.
`VERIFY` requires a live browser/integration read through the current Codex chat.
MCP configuration alone never produces a ready result. The skill performs those
agent checks and gives the combined assessment when asked to check readiness.

Exit codes: 0 for all requested shell checks passing, 1 for a blocker or pending
verification, 2 for invalid arguments. JSON output uses the same statuses and
includes the scope. No output contains raw command errors, tokens, or service
records. Identity checks may use a credential provider's normal refresh/cache.

The command does not run model requests, change permissions, sign in, build, or
boot devices. It does not prove that the laptop will remain online, that native
desktop control works while locked, or that deployment/signing permissions work.

## Repairing the terminal Codex installation

`remote-ready` reports a broken PATH installation even if the desktop app works.
For an npm installation, use the [official CLI installation method](https://learn.chatgpt.com/docs/codex/cli):

```sh
npm install -g @openai/codex --include=optional
codex --version
codex login status
```

Check `command -v codex` in a fresh terminal if an older Node installation still
wins on PATH. The macOS desktop app may provide a working diagnostic fallback at
`/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex`; using that
fallback does not repair the terminal installation.

On 30 October 2026, replacing the incomplete npm installation with `0.166.0`
restored the missing Apple Silicon executable and preserved the existing login.

## Checks for this tooling

```sh
python3 -m unittest discover -s codex/tests -v
```
