---
name: testflight-release
description: Build, upload and verify internal TestFlight releases from the terminal while Dan is away from his Mac. Use for TestFlight delivery, App Store Connect API authentication, signing setup and recovery of interrupted uploads.
---

# TestFlight delivery

Deliver the requested source revision to the intended internal tester group using
the project's existing release workflow. Prefer API authentication and CLI tools
over Organizer or browser automation. Keep an established Fastlane pipeline.

## Before building

- Read the app's release instructions. Resolve its app ID, bundle ID, Apple team
  and internal group ID. Verify these against Apple; a local profile name is not
  an account or app permission boundary.
- Coordinate with any other agent releasing the same app. One agent owns build
  numbers and upload; do not start a competing release to test this skill.
- Use `asc version` and the installed command's `--help`. The shared helper is
  tested with ASC 5.17.1. Its upstream skills (`asc-xcode-build`,
  `asc-signing-setup`, `asc-testflight-orchestration`) cover command details.
- API keys and signing identities are different. Read
  [setup.md](references/setup.md) for missing auth or signing. Reuse working
  credentials; no Apple Account password or Safari session is needed for the
  routine public-API flow. Never use a Sign in with Apple key for ASC.

## Build and export

Use [build.md](references/build.md) for the archive/export recipe. Run the app's
relevant checks, commit its source and record the SHA before archiving. Give each
upload a unique build number, including concurrent and in-flight uploads in the
lookup. Pass build-number overrides to Xcode rather than changing source solely
for a beta. Keep the archive and signed IPA until delivery is verified.

For this internal-only route, export with `testFlightInternalTestingOnly=true`,
`destination=export` and `manageAppVersionAndBuildNumber=false`. Preserve the
app's actual encryption declaration; never change compliance answers simply to
make an upload pass. Public release and external-testing requests need their own
explicit scope and workflow.

## Upload and verify

The `testflight` helper installed from this repository validates app/bundle/group
identity, rejects external groups, records the IPA hash and source commit, and
separates upload from resumable processing/distribution:

```sh
testflight check --app APP_ID --bundle-id BUNDLE_ID --group-id INTERNAL_GROUP_ID
testflight upload --app APP_ID --bundle-id BUNDLE_ID --group-id INTERNAL_GROUP_ID \
  --ipa /absolute/path/App.ipa --source-sha COMMIT_SHA \
  --receipt /private/path/release.json
testflight resume --receipt /private/path/release.json
testflight status --receipt /private/path/release.json
```

`--source-sha` records the caller's archive provenance; the helper cannot prove
which source produced a binary. Supply the SHA actually archived, not a later
documentation commit. `upload` does not wait or distribute. `resume` waits for up
to 45 seconds, then adds the processed build to the checked internal group and
verifies availability. Exit 7 means still pending, not success. `status` performs
only Apple reads. All commands emit JSON; failures never print raw auth output.

For an existing upload without a receipt, use `testflight track` with the app,
bundle and group flags plus `--version`, `--build-number`, `--source-sha` and a
new `--receipt`. It reads Apple and records an unknown IPA hash as null. It never
uploads or assigns groups. Do not invent an IPA hash for an Organizer upload.

After any uncertain upload, use the existing receipt and exact version/build
lookup. Do not blindly upload again or select an unspecified latest build. If
Apple reports failure, retain the receipt, inspect the protected diagnostic log
and repair the cause before allocating another build. A timeout alone is not a
reason to rebuild. Bound follow-up polling; use a supported monitor when work
must continue after the turn.

Use `remote-handoff` for the early simulator video, install instructions and
focused device checks. Report **uploaded**, **processing**, **available to
install**, and **installed/verified on device** distinctly. The last status
requires actual device evidence or Dan's confirmation.

## CI

Read [ci.md](references/ci.md) when moving delivery to macOS CI. Reuse the same
API identity checks and exact-build receipt. CI continuing after the laptop
sleeps does not keep a laptop-hosted Codex chat reachable.
