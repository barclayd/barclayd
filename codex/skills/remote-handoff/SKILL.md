---
name: remote-handoff
description: Prepare a phone-accessible handoff of coding changes for Dan, with a website preview, app demonstration, or installable beta and focused review steps. Use when Dan is reviewing remotely, asks to see or test a build from his phone, or needs an early video while TestFlight is being prepared. Does not move chats between hosts.
---

# Remote handoff

Give Dan something he can open, watch or install from his phone, with enough
context to review the change. Use the project's existing build and delivery
workflow. Keep committing, pushing and opening/updating the PR under Dan's
standing instructions; merging remains with Dan.

## Choose the delivery route

Read the repository's release/testing instructions and establish the relevant
branch, source revision and target environment. Use `remote-ready` if access is
uncertain, selecting only the capabilities this task needs.

| Platform | Primary handoff | Early visual feedback |
| --- | --- | --- |
| Website | An accessible HTTPS preview for this revision | Screenshots; video for motion or a multi-step flow |
| iPhone app | An internal TestFlight build available to Dan | A short simulator or device recording while signing, TestFlight setup or Apple processing continues |
| Mac app | A recording of the changed flow; a signed build when the project calls for one | Focused screenshots and video that can be reviewed on a phone |

Read [platforms.md](references/platforms.md) for the relevant platform's capture
and delivery details. Do not set up a new hosting service or replace a release
pipeline when an existing route works.

## Deliver the preview early

For an iPhone app, supply a short demonstration as soon as a meaningful flow can
be shown, **while TestFlight is being set up or processing**. Do not wait for an
installable build before sharing useful visual progress. This also applies when
a website preview or Mac package is still being prepared.

- Show the actual changed application. Identify simulator versus physical device,
  and label mock data or simulated behaviour. A design mock-up is not a working
  app demonstration.
- Prefer one focused recording, roughly 20–60 seconds when that is enough. Show
  the starting state, interaction and result. Capture the app window or relevant
  viewport at a size readable on a phone, with synthetic task data.
- Record the source commit and, for an app, version/build and device/OS alongside
  the media. If it shows uncommitted work, say so; do not attribute it to a commit
  that lacks those changes. Refresh evidence when later changes invalidate it.
- Check that the recording is finalised, playable and actually shows the result.
  If capture is unavailable, provide screenshots and explain the specific limit
  while continuing the remaining build/delivery work.

An early preview is a progress update, not completion of the requested
installation. State what remains and continue the authorised work.

## Make the evidence reachable

Use supported chat media when it reaches the phone, and include a durable HTTPS
link in the handoff. For repository work, prefer media attached to its PR using
the `pr-and-commit-style` skill. Do not rely solely on `/Users/...`, `localhost`,
an expiring build log, or a raw simulator bundle.

Inspect screenshots/recordings before uploading. Use the authorised destination
and its intended audience; exclude credentials, private notifications and real
customer content from public PR media. Do not make a private preview public to
avoid a sign-in requirement.

Verify the uploaded attachment or deployment exists and the URL is the actual
returned link. Check access using the intended account when possible. If phone
playback or phone sign-in has not been exercised, say so instead of claiming it
has. Do not commit large media files just to embed them in a PR.

## Track delivery through availability

Distinguish a **visual preview**, **build/deployment still processing**, **available
to test**, and a **blocker**. Do not describe an upload, green build or simulator
launch as a beta being available on Dan's phone.

Keep following the specific deployment/build until it is available or there is a
concrete blocker. If a follow-up must outlive the current turn, use a supported
monitor or scheduled follow-up within the authorised task, with the exact build
identifier, a bounded lifetime and a stopping condition. Discover the available
tool and follow its schema. Notify on readiness, failure or required user action;
stay quiet while unchanged. Only promise a later notification after confirming
the follow-up exists. A detached shell process alone is not a notification.

Reuse existing authorisation for previews and internal betas. This workflow does
not itself authorise production releases, public beta invitations, broader
account access or changes to signing credentials. For a blocked capture/upload,
preserve usable evidence and report the smallest remaining action; do not invent
a link, silently change the audience or repeatedly create duplicate builds.

## Handoff in the chat

Lead with the usable result, keeping the message short enough to review on a
phone. Include what is applicable:

- **Open / install:** the preview or PR link, or TestFlight invitation/open-app
  instructions with the exact version/build.
- **Watch:** the demonstration and what it proves; identify early previews.
- **Try:** a few concrete actions and expected results, plus setup where needed.
- **Version:** the PR, source commit and app build so feedback identifies the work.
- **Remaining:** processing state, known limitations and any device checks still
  needed. Separate agent verification from Dan's hands-on acceptance.

Keep review steps and status in the chat or the project's testing document;
preserve Dan's concise PR style. Update the same PR and handoff when the build
becomes available. Accept screenshots, recordings or descriptions as feedback
and tie fixes back to the reported build.
