---
name: aws-sso-login
description: Sign in to AWS CLI with IAM Identity Center (SSO), or recover an expired AWS SSO session, using a device link Dan can authorise on his phone while Codex keeps the login command running on his laptop. Use for aws sso login and AWS access blocked by expired SSO credentials.
---

# AWS SSO login from a phone

Dan's agreed workflow is to keep his laptop awake and online, run AWS CLI there,
send him the CLI's device authorisation link in this chat, and continue after he
approves on his phone. Use the existing AWS profiles and permissions. The default
profile for an unspecified AWS login request is `production`; honour another
profile when the user names it or the active task clearly establishes it.

## Workflow

1. For an AWS access task, first check whether the selected profile already works:

   ```sh
   aws sts get-caller-identity --profile production --output json --no-cli-pager
   ```

   If it succeeds, continue the authorised task without an unnecessary login.
   If the user explicitly requests a fresh login, perform it even if access works.
   Distinguish an expired SSO session from a network error, missing profile, or
   service permission failure; reauthentication does not fix every access error.

2. Start the device flow on the same host that will run subsequent AWS commands:

   ```sh
   aws sso login --profile production --use-device-code --no-browser
   ```

   Replace `production` consistently when a different profile was selected. Use
   an execution tool that returns a resumable process/session ID while the CLI
   waits. With `exec_command`, use a short initial `yield_time_ms`, retain its
   `session_id`, and resume with `write_stdin`. Keep this process running while
   the user authorises; do not launch a second login merely because it is waiting.

3. Immediately send the actual link and code printed by this invocation:

   > Open [AWS sign-in](ACTUAL_VERIFICATION_URL) on your phone and authorise it.
   > If asked for a code, enter **ACTUAL_USER_CODE**. The command is waiting on
   > your laptop; I'll verify access when approval completes.

   Prefer the printed URL that autofills the code. The link may open in the
   phone's browser from Codex. Device authorisation supports another device;
   `--no-browser` alone does not make the default PKCE flow suitable for this.
   Do not substitute the CLI's default PKCE login URL, open a desktop browser,
   request passwords or MFA codes in chat, or save device codes in skill files.

4. Resume the same CLI process with bounded waits (at most 30 seconds each).
   Success requires the CLI to finish successfully, not just a user saying they
   approved or a browser displaying a success page. If the request expires or is
   denied, report that outcome. Generate a fresh request when the user is ready;
   do not loop through new requests unattended. Never reuse a previous code.

5. After CLI success, run `sts get-caller-identity` again with the same profile.
   Compare its account ID with the profile's configured `sso_account_id` (read
   with `aws configure get sso_account_id --profile production`) and check the
   returned role is consistent with the configured `sso_role_name`. Stop on an
   unexpected identity. Report verified access and resume the original task.

## Operational boundaries

- The AWS CLI stores its session in its normal local cache. Later AWS commands
  must use this same host/user and selected profile. A phone approving the link
  does not transfer credentials to an unrelated cloud chat or computer.
- Keep the laptop and Codex host awake and online. No background schedule,
  infrastructure, IAM policy, SSO duration, or AWS profile changes are needed.
- This agreement authorises the requested login flow. Subsequent AWS operations
  remain scoped to the user's task; do not silently select a break-glass role.
- AWS may require a fresh sign-in or MFA on the phone. The workflow removes the
  need to touch the laptop; it does not promise permanent unattended access.
- Do not read or print cached access tokens, refresh tokens, secret keys, or
  passwords. Identity checks do not require exposing credential material.

Reference: [AWS CLI IAM Identity Center authentication](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html).
