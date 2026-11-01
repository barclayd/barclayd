# Codex setup

These skills can also be linked into Claude Code with
`python3 claude/install-shared-skills.py` from this checkout. See
[Claude setup](../claude/SETUP.md) for prerequisites and invocation syntax.

## Apple app architecture

Install the architecture skill from this checkout:

```sh
./codex/install-app-architecture.sh
```

Invoke `$apple-app-architecture` for a new app foundation, shared Swift package
design or migration. It covers thin Apple app shells, vertical feature products,
Bun/Hono/Zod APIs on Cloudflare, API-owned OpenAPI contracts and preserving
existing storage/sessions during extraction. The guides distinguish reusable
preferences from product-specific decisions and include both new-app and
migration workflows.

The installer links the skill into `$CODEX_HOME/skills` or `~/.codex/skills`, is
safe to rerun and preserves conflicting installations. It needs no Apple or
Cloudflare credentials. Keep this checkout available and reload skill discovery
if needed; existing chats can read
`codex/skills/apple-app-architecture/SKILL.md` directly.

## TestFlight from the terminal

Install ASC and the global skill/command from this checkout:

```sh
brew install asc
asc install-skills
./codex/install-testflight.sh
```

The installer links `testflight` into `~/.local/bin` and `testflight-release` into
`$CODEX_HOME/skills` or `~/.codex/skills`, preserving other installations. Set
`TESTFLIGHT_BIN_DIR` to choose a different command directory. Python 3.11+ is
required. Keep this checkout available. An existing chat can read the skill at
`codex/skills/testflight-release/SKILL.md` immediately; discovery may need reload.

The helper is tested with the ASC version pinned in `testflight-toolchain.json`.
CI uses `scripts/install_asc.py --bin-dir DIRECTORY` to install a checksum-pinned
binary without replacing another installation. Update the pin, upstream hashes
and helper compatibility together when upgrading.

```sh
testflight check --app APP_ID --bundle-id BUNDLE_ID --group-id INTERNAL_GROUP_ID
testflight upload --app APP_ID --bundle-id BUNDLE_ID --group-id INTERNAL_GROUP_ID \
  --ipa /private/path/App.ipa --source-sha FULL_SOURCE_SHA \
  --receipt /private/path/release.json
testflight resume --receipt /private/path/release.json
testflight status --receipt /private/path/release.json
```

Upload records provenance supplied by the caller and the actual IPA hash before
contacting Apple. It does not build, sign or infer source from an IPA. A failed
upload leaves its receipt for exact-build recovery. Reusing an existing receipt
for upload fails, so an interrupted command cannot blindly upload twice.
`resume` performs a bounded processing check, assigns the verified internal group
when needed and verifies availability; `status` only reads Apple. Exit 7 means
pending. Exit 1 means a blocker. JSON status `api_access_verified` says nothing
about signing; `available_to_install` requires Apple's processed, unexpired build,
internal testing state and group membership. Neither claims device installation.

For a build uploaded elsewhere, `testflight track` takes the same app/group flags,
plus `--version`, `--build-number`, `--source-sha` and a new `--receipt`. It records
an unknown IPA hash as null and verifies the existing build without uploading.

Use `$testflight-release` for setup, archive/export and handoff. Its references
cover API keys, manual distribution signing and the reusable macOS CI workflow.
Keys, signing identities, passwords, logs and archives belong outside Git. The
helper keeps receipts/logs private (0600) and never prints raw auth failures.
One local helper per app can run at a time; coordinate local releases with CI
because the host lock is not a cross-machine build-number reservation.

## Review from a phone

Install the handoff skill from this checkout:

```sh
./codex/install-remote-handoff.sh
```

The installer links `remote-handoff` into `$CODEX_HOME/skills` or
`~/.codex/skills`, is safe to rerun, and refuses to replace another installation.
Keep this checkout available. `codex/AGENTS.md` contains the standing handoff
instruction; apply that section to the global `~/.codex/AGENTS.md` while preserving
any other instructions. The installer does not overwrite global instructions.

Ask "prepare a handoff I can review from my phone" or invoke `$remote-handoff`.
It selects website previews, internal TestFlight builds or Mac demonstrations
using the project's existing delivery setup. iPhone work includes an early video
while TestFlight is being prepared, followed by the build when it is available.
An existing chat may need an explicit skill invocation or reload to discover a
newly installed skill.

The skill coordinates existing tools; it does not install a recorder, configure
Apple signing, provision hosting or enable macOS permissions. Those prerequisites
belong to the relevant project/setup task. First use should verify that the
chosen media and preview links open on Dan's phone.

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
