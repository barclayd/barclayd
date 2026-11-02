# duoctl (vendored)

[skarol/duoctl](https://github.com/skarol/duoctl) v0.2.1, commit `c6ff3e9`, MIT (see
[LICENSE](LICENSE)). Copied unchanged from `skills/duoctl/scripts/` so the code that
runs is the code that was reviewed.

| File | sha256 |
|---|---|
| `duoctl` | `2cac62ae4de41403e94ed879d086e8e2bce4a0722fdef2b70ee51361be0368db` |
| `duoctl-helper.m` | `be2c6dc803d8488d338fdc8e7930b8a2dfe0d8e25685139b5069a4ca7c1bd6c9` |

What it does, from reading both files:

* `duoctl` (Python) only runs `xcrun simctl`, `xcrun devicectl`, `xcode-select`,
  `codesign` and, for `--label`, `--id` and `elements`, `axe`
* Its first run compiles `duoctl-helper.m` with the simulator SDK's clang into
  `~/.cache/duoctl`, ad-hoc signs it and runs it inside the simulator with `simctl spawn`
* The helper sends the hinge and orientation HID events Device Hub sends, and clones the
  live display's touchscreen to deliver touches to it. It has no network code

To update, read the upstream diff, copy both files from the new tag, and update the
version, commit and hashes here.
