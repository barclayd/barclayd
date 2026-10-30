---
name: remote-ready
description: Check whether Dan's laptop is ready for a coding task controlled from his phone. Diagnose CLI, GitHub, AWS, browser, Xcode, and requested integration access before work starts or when tools fail. Use for remote readiness checks; do not automatically check unrelated accounts or start logins.
---

# Remote readiness

Use the read-only `remote-ready` command, then complete any requested browser or
integration probes in this chat. The laptop is expected to remain awake and online.

## Scope and command

Infer the required capabilities from the active task. The default checks Codex CLI,
local Codex sign-in, and an authenticated GitHub API read. Add only relevant flags:

```sh
remote-ready --repo barclayd/barclayd --aws-profile production
remote-ready --xcode --browser --mcp sentry --json
```

If the command is not installed, run `scripts/remote_ready.py` from the `codex`
directory containing this skill (resolve the skill's symlink to find it). Python
3.11+ is required. Installation instructions are in `codex/SETUP.md`.

Use the task's AWS profile; when the user asks for an unspecified AWS login, Dan's
default is `production`. Do not infer broader privileges from a successful login.

The command exits 0 only when all selected shell checks pass. Exit 1 means there
is an issue or an agent probe still required; exit 2 indicates invalid arguments.
It does not start sign-in, change configuration, build, boot a simulator, or run a
model. Credential providers may renew their normal caches during identity reads.

## Complete the live probes

`VERIFY` is not success. A saved configuration, discovered tool name, or cached
OAuth token does not establish that the current chat can use a service.

- **Browser:** use the available browser tool to list tabs and read the current
  state of one task-relevant existing tab. Follow that tool's setup rules. Do not
  navigate, open an unrelated page, or change browser settings for this check.
  If there is no suitable tab, report that the connection responds but page access
  remains untested. Browser success does not prove native desktop control.
- **Integrations:** discover the actual tools in this chat and follow their
  required skills. Make a small authenticated read for each requested service,
  such as Sentry's organisation listing or LambdaTest's first project page.
  For Payload, use one known page with minimal fields. For Datadog, follow its
  tool/skill guidance and use a bounded read. Summarise access, not returned data.
- **Xcode:** the shell check establishes the toolchain and simulator availability.
  Build, signing, Xcode MCP, and simulator UI control are separate capabilities;
  test them only when needed by the task and report any untested capability.

Do not create a fresh chat, start an agent/model, or implement private app-server
RPC calls to work around missing tools. Use available connected tools or explain
that a new/reloaded session is needed to expose a configured integration. A
separate local MCP and an account plugin can have different authentication states.

## Report and recovery

Give a short list of capabilities proven ready, blockers with one next step each,
and anything still unverified. Keep these distinctions:

- CLI version works / local sign-in exists / actual service read works.
- AWS account and role match / the requested service operation is permitted.
- GitHub API reports push permission / actual PR creation and branch rules work.

For an expired AWS SSO session, use the installed `aws-sso-login` skill when login
is authorised: send the fresh device link, keep the command alive, and verify the
same profile afterwards. For Codex, `codex login --device-auth` is the phone flow.
Other services need their own supported authentication method; do not assume a
localhost callback link will complete on a phone.

Access denied, missing tools, and network failures are not all login failures.
Do not repeatedly request sign-in or broaden permissions to make the report green.
The readiness request itself does not authorise installing tools or changing
permissions. If the user has already requested repair or login, proceed within
that scope and rerun only affected checks.

Never print tokens, credential files, raw auth errors, or private tool responses.
