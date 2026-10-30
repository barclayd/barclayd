# Platform delivery

Read only the section relevant to the task. Prefer tools and release scripts
already available in the project; inspect their help before relying on options.

## Websites

Use the repository's PR/staging deployment and identify the deployment for the
current source commit. A branch alias can move to a newer commit; use an immutable
deployment link where available and retain the source revision in the handoff.
Open the route and exercise the changed flow, including the relevant mobile
viewport. An HTTP 200 or successful deployment alone does not prove the UI works.

Use the built-in browser or connected browser tools under their own instructions.
For recordings, use an available browser recorder, such as Chrome DevTools
`screencast_start` / `screencast_stop`, or the project's existing browser-test
capture. Respect whichever browser-control surface the current task requires.

Send an HTTPS URL the phone can reach, with any required sign-in instructions.
An existing approved private tunnel can work for a local-only project, but report
its dependence on the host/server remaining online. Do not open public tunnels or
remove access controls as an implicit fallback. If hosting is not configured,
send captured evidence first and identify the missing deployment setup.

## iPhone apps

### Early recording

Use the app's existing simulator build/run workflow. Select a specific simulator
UDID from `xcrun simctl list devices available`, rather than assuming `booted`
belongs to this task. Do not replace another agent's build or operate its active
simulator; reuse a suitable task device or choose an isolated one.

For an already selected and running simulator, the capture commands are:

```sh
xcrun simctl io "$simulator_udid" screenshot "$capture_dir/preview.png"
xcrun simctl io "$simulator_udid" recordVideo --codec=h264 "$capture_dir/preview.mp4"
```

Set the task-specific variables from the observed simulator and a unique output
directory. Keep the recording command's process/session handle. Wait for
`Recording started`, perform the flow through the available supported UI tools,
then send SIGINT to that recording process and wait for it to finish finalising
the file. Do not use `killall` or SIGKILL, and do not leave recording running while
waiting for Apple. Use supported media inspection to verify the finished output.

Label the video as a simulator preview. Simulator evidence does not establish
physical microphone/audio behaviour, background execution, device permissions,
notifications or the final TestFlight installation. Include the device-only
checks relevant to the feature in the eventual handoff.

### Internal TestFlight delivery

Use the project's existing trusted build/release workflow and its authorised
Apple account. Verify the app record, signing/provisioning for the app and its
extensions, upload access, and Dan's eligible internal tester group. Start this
setup early while implementation and simulator demonstrations proceed.

Build and upload the tested source revision with a unique version/build pair.
Track that exact build through Apple processing, required compliance information
and assignment to the intended internal group. Retain the build/run link and
source commit; check the current build instead of distributing an unspecified
"latest" build. Upload credentials and upload success do not prove distribution
permissions or tester availability.

Internal testers must be eligible App Store Connect users with app access. Use
their actual invitation or tell an already enrolled Dan to open TestFlight and
select the named app/build. Do not invent a public join link: public invitation
links are an external-testing route with different review requirements.

Prefer the existing noninteractive App Store Connect authentication when it
supports the necessary operations. API authentication does not replace signing
certificates/profiles or first-time account setup. Do not echo or put signing
secrets in recordings, chat, source control or build artifacts.

Use "available to install" after confirming processing and internal group access.
Only claim installation or physical-device acceptance after actual evidence from
that device or Dan. While setup or processing is incomplete, send the early video
and report that installation is pending. Do not give a guaranteed Apple processing
time or switch to external testing to manufacture a shareable link.

## Mac apps

Use supported Computer Use to exercise the actual changed app and capture its
window. A video is the main review artifact while Dan is on his phone; a Mac
installer is useful for later hands-on testing, not installation on an iPhone.

For motion or multi-step behaviour, use an existing permitted screen recorder or
the project's capture tooling. Native Computer Use screenshots do not by
themselves imply that a video-recording tool is available. ScreenCaptureKit is an
option for a deliberately configured recorder, not a reason to build a new
recording app for every task.

Screen Recording, Accessibility and target-app permissions may need one-time
setup. Codex's macOS Locked use is opt-in; do not assume that an awake but locked
Mac permits UI capture, or try to bypass missing system permissions. Report the
specific blocker and deliver any usable evidence while other work continues.

When a distributable Mac build is required, follow the project's signing and
notarisation workflow and link the exact preview artifact/version. Keep its
source revision aligned with the demonstrated build. Preserve existing beta and
production release boundaries.

## Media attachment

Read `pr-and-commit-style` before modifying a PR. With a supported GitHub CLI,
`gh pr edit <pr-url> --attach <absolute-video-path>` appends a video without
replacing the existing body. Retrieve the resulting body/link and verify the
attachment. An attachment failure can follow a successful PR update; inspect the
PR before retrying, and retry only missing media. Check CLI help if the installed
version lacks the option; use another supported authorised upload route instead
of guessing a GitHub upload API.

## Sources

Operational guidance checked on 30 October 2026. Recheck the relevant official
documentation when a tool, authentication method or distribution rule differs.

- [Codex remote connections](https://learn.chatgpt.com/docs/remote-connections)
- [Browser testing](https://learn.chatgpt.com/docs/browser)
- [Computer Use and Locked use](https://learn.chatgpt.com/docs/computer-use)
- [Internal TestFlight testers](https://developer.apple.com/help/app-store-connect/test-a-beta-version/add-internal-testers/)
- [External TestFlight testers](https://developer.apple.com/help/app-store-connect/test-a-beta-version/invite-external-testers/)
- [TestFlight upload automation](https://docs.fastlane.tools/actions/upload_to_testflight/)
- [Mac screen capture](https://developer.apple.com/documentation/screencapturekit/capturing-screen-content-in-macos)
- [GitHub PR media attachments](https://cli.github.com/manual/gh_pr_edit)
