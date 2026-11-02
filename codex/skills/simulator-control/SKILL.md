---
name: simulator-control
description: Drive and capture iOS simulators from the command line, with no one at the Mac and without Device Hub, so app work can be checked and shown to Dan while he's away from his laptop. Covers picking a task's own simulator, installing and launching builds, reading the screen and tapping (AXe), folding, rotating and touching the iPhone Duo simulator's inner screen (duoctl), and screenshots and video sent to his phone. Use whenever you verify UI on a simulator yourself.
---

# Simulator control

Check your own work on a simulator, then show Dan what it looks like on his phone.
Everything here runs from the shell: no Device Hub window, no clicks on the Mac's
screen and no person at the laptop.

| Need | Tool |
|---|---|
| Create, boot, install, launch, open URLs, appearance, status bar, location, push | `xcrun simctl` |
| Screenshots and video | `xcrun simctl io` |
| Read what's on screen; tap, swipe and type on an iPhone (or the Duo's cover screen) | `axe` |
| Fold, unfold and rotate the iPhone Duo; tap and swipe its inner screen | `duoctl` |
| Get media to Dan | the chat's file-sending tool, or PR attachments via `remote-handoff` |

If `axe` or `duoctl` is missing or blocked by a permission check, see the setup docs
(`claude/SETUP.md` or `codex/SETUP.md` in Dan's `barclayd` repo). Don't work around a
blocked command: report it and carry on with `simctl`.

## Use your own simulator

- Pick or create a simulator for this task and always pass its UDID. Never use
  `booted`: other agents, release scripts and Dan's own windows share the Mac.

  ```sh
  xcrun simctl list devices available
  xcrun simctl create "TripSplit Duo" "iPhone Duo" com.apple.CoreSimulator.SimRuntime.iOS-27-1
  xcrun simctl boot "$udid" && xcrun simctl bootstatus "$udid" -b
  ```

- Don't drive a simulator another agent or a release script is using, and never
  install on, launch on or capture a physical device unless Dan says it's free.
- Leave Device Hub alone. Nothing here needs it, and another agent may be using it
  to show a device.
- Never capture the Mac's screen (`screencapture`, window grabs) for simulator
  evidence. It can catch Dan's other windows. Use `simctl io`, `axe` or `duoctl`.

## Install and launch

```sh
xcrun simctl install "$udid" path/to/App.app
xcrun simctl launch --terminate-running-process "$udid" com.example.app [args...]
xcrun simctl openurl "$udid" "myapp://route"
xcrun simctl ui "$udid" appearance dark
xcrun simctl status_bar "$udid" override --time 9:41 --batteryState charged --batteryLevel 100
```

Prefer the app's own launch arguments (demo data, deep links to a screen) over
long tap sequences. They're faster and don't break when a layout moves.

## Read the screen and tap

```sh
axe describe-ui --udid "$udid"            # accessibility tree with frames, in points
axe tap --label "Continue" --udid "$udid"
axe tap --id settings.close --udid "$udid"
axe tap -x 200 -y 400 --udid "$udid"
axe swipe --start-x 200 --start-y 700 --end-x 200 --end-y 300 --udid "$udid"
axe type 'Hello' --udid "$udid"
axe button home --udid "$udid"
```

Check `axe <command> --help` before relying on a flag. AXe exits 0 even when a touch
misses, so confirm every action changed the screen with `describe-ui` or a
screenshot.

## iPhone Duo

The Duo has two displays: the cover (outer) screen is display 1 and the inner screen
is display 3. Only the live one renders; the other captures black. AXe, idb and
XcodeBuildMCP send every touch to the cover screen, so on an unfolded Duo they
report success and nothing happens ([AXe #74](https://github.com/cameroncooke/AXe/issues/74)).
Use `duoctl` for anything on the inner screen, and for folding.

```sh
duoctl -d "$udid" state                    # hingeAngle, activeScreen (cover|inner), orientation, sizePoints
duoctl -d "$udid" open                     # 180°, waits for the inner screen
duoctl -d "$udid" close                    # 0°, waits for the cover screen
duoctl -d "$udid" half                     # 90°
duoctl -d "$udid" hinge 130 --duration 1.5 # any angle; --duration animates it
duoctl -d "$udid" rotate portrait          # portrait | landscape | portrait-upside-down | landscape-flipped
duoctl -d "$udid" elements                 # labelled elements with frames (uses AXe)
duoctl -d "$udid" tap --label "Back"       # or: tap <x> <y>, tap --id <identifier>
duoctl -d "$udid" swipe 330 800 330 300 --duration 0.4
duoctl -d "$udid" long-press 120 340 --duration 1
duoctl -d "$udid" screenshot "$out/inner.png"
```

- Always pass `-d`. With several Duos booted it refuses to guess.
- Coordinates are interface points of the live screen, the same space `elements` reports.
  Orientation names describe the interface: unfolded, the inner screen's default is
  `landscape`.
- Every change prints `state` afterwards, and fails if the fold or rotation didn't
  happen. Read it rather than assuming.
- The first run compiles a small helper into `~/.cache/duoctl`.
- Never set the hinge with a tool that jumps straight between closed and open. On
  the iOS 27.1 runtime that can stop the simulator switching screens until it's
  recreated. `duoctl` always sweeps.
- `simctl io screenConfig ... power` doesn't fold the phone. It only blanks a display.
- Device Hub's hinge slider doesn't follow changes made by `duoctl`.

For layout checks, go through the poses the design needs: closed portrait, closed
landscape, open landscape, open portrait and half open. Open and close mid-task to
check that state carries across. The `iphone-duo-design` skill has the full list.

## Capture

```sh
xcrun simctl io "$udid" screenshot --display=3 "$out/inner.png"   # Duo: 1 cover, 3 inner
xcrun simctl io "$udid" recordVideo --codec=h264 --display=3 "$out/flow.mp4"
```

On other iPhones, leave out `--display`.

- Start `recordVideo` in the background, wait for `Recording started`, run the flow,
  then send SIGINT to that process and wait for it to finish writing. Never use
  SIGKILL or `killall`.
- For a fold, record each display separately, because each recording covers one
  display. Use `duoctl open --duration 1.5` so the change is visible.
- Look at every screenshot and video before sending it. Use demo data, and leave out
  notifications and anything personal.

## Send it to Dan

- **In Claude Code:** send the files with `SendUserFile` so they reach his phone.
  Otherwise, attach them to the PR as `pr-and-commit-style` describes.
- **Labelling:** label it a simulator preview, with the source commit and the
  device and OS. Follow `remote-handoff` for the rest of the handoff.
- **What it can't prove:** simulator evidence doesn't prove an installed TestFlight
  build, real touch feel, what a hand covers on the Duo, or anything only the
  hardware does.

## Working while Dan is away

- **What it needs:** the Mac must stay awake, online and logged in. `simctl`, `axe`
  and `duoctl` don't need Device Hub or a visible window.
- **Locked Mac:** whether each tool works while the Mac is locked hasn't been
  confirmed yet. Test it the first time it matters, and report what didn't work.
- **Settings:** never change sleep, lock or update settings without asking.
- **Xcode updates:** an update restarts CoreSimulator and shuts simulators down. Boot
  your simulator again, then reinstall and relaunch before carrying on.
- **When a tool stops working:** report the exact command and error. Keep going
  with whatever still works, such as `simctl` screenshots from launch arguments.
