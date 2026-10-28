---
name: pr-and-commit-style
description: Dan's personal style for git commit messages, branch names, PR titles and PR descriptions. Use whenever writing a commit message, naming a branch, opening a PR (`gh pr create`), or writing/editing a PR title or body. Visual changes need screenshots or video in the PR.
---

# PR and commit style

Write commits and PRs the way Dan wrote them before AI tools started writing them. This guide was distilled from ~1,900 PRs and ~8,100 commits Dan wrote between 2019 and March 2026. It weights the 2024 to early 2026 period most heavily.

The overall feel is **terse, lowercase and to the point**. If it reads like a generated report, it's wrong.

## Commit messages

Format: `type: description`

- Use one line. Don't add a body (99% of Dan's commits have none).
- Make it all lowercase, except for proper nouns and identifiers (`iOS`, `JIRA`, `README.md`, `InventoryView`).
- Don't add a scope, so no `feat(api):`. Don't end with a full stop.
- Keep it short. Aim for 15–30 characters and rarely go past 50.
- Name the change. Don't describe the implementation.

Types, from most to least used:

| type | used for |
|---|---|
| `chore` | the default: tweaks, refactors, config, deps, renames, small fixes |
| `feat` | new behaviour or UI |
| `fix` | a bug |
| `style` | css, lint, formatting |
| `docs` | README and docs |
| `deploy` | deployment, infra and pipeline changes |
| `ci` | CI workflows |
| `test` | tests |
| `refactor`, `perf` | occasionally |
| `wip`, `temp`, `debug`, `spike` | throwaway commits mid-branch |

How the description is worded:
- **Short imperative verbs:** add, update, remove, improve, fix, bump, use, handle, tweak, rename, prevent, support, return.
- **Bare noun phrases are fine:** `feat: shopping list`, `fix: navbar burger icon`, `feat: cost calculator`.
- **"better" and "more" phrasings are fine too:** `chore: better image sizing`, `chore: better auth sign up`.
- **Number repeat passes:** `feat: improve tabs ux 2`.
- **Put a short reason after a dash** if it really helps: `chore: remove recent images - to be picked up post mvp`.

For work on a Jira ticket, the ticket key can replace the type: `alm-1234: fix accidental form validation`. Use lowercase for new work.

Add a body only for a `BREAKING CHANGE:` note, or when the reason is not obvious and matters later (e.g. pinning a dependency down on purpose). Keep it to one or two plain sentences with no bullets.

Commit little and often rather than writing one big commit with a long message.

Good examples:

```
feat: add shopping item
chore: bump deps
fix: parsing of inventoryItem
chore: prevent accidental deployments
refactor: rename kitchenui
feat: make screen view dynamic across device size
chore: restrict data creation to api keys only
fix: prefetch genmoji only once per app load
docs: dark mode
setup: playwright
```

## Branch names

`type/kebab-case-description`, e.g. `feat/push-notifications`, `chore/bump-deps`, `fix/review-card-animation-height`.

For Jira work, use `alm-1234/kebab-case-description`.

## PR titles

Use the same format as a commit subject: `type: short lowercase description`, typically around 20–25 characters. For Jira work, use `alm-1234: description` with a lowercase key, matching the branch.

```
feat: push notifications
chore: bump to vite 6
fix: klarna typo
deploy: gcp
alm-1234: redirect for old partner url
```

## PR descriptions

Use this template:

```markdown
# Changes

* Adds `thing`
```

The heading is literally `# Changes`, followed by a blank line and then `*` bullets. Write bullets, never prose. If something needs explaining, it becomes another bullet or a nested `-` sub-bullet. Most PRs need 1–3 bullets. Even a big PR is a handful of bullets, not an essay. Most of Dan's PR bodies are under 300 characters.

### Bullets

- Start with a third-person present-tense verb: **Adds**, **Updates**, **Removes**, **Fixes**, **Improves**, **Bumps**, **Supports**, **Introduces**, **Renames**, **Refactors**. Something like "Uses X rather than Y" is fine too. A bare noun phrase is OK for tiny PRs (`* Programmatic routing`).
- Keep each bullet to one line, as a sentence fragment with no full stop.
- Wrap identifiers, packages, files, commands and CSS classes in backticks. Write versions as `` `vite`@`6` ``.
- Use `=>` for mappings or renames: `` `/old-path` => `/new-path` ``.
- Put the **why** inline, in parentheses or a trailing clause. Don't give it its own section:
  - `(represents 1.25rem/2px)`
  - `to prevent a race condition where ...`
  - `(due to ...)`
- When something is left for later, say so briefly: `Routing to follow`.

### Images and video

Visual changes get media. Dan almost always includes it for UI work.

- **Images** for anything visual: UI, layout, styling, emails, dashboards.
- **Video** when a still image can't show the change: animations, transitions, multi-step flows, or behaviour on a device.
- Put media below the bullets. When there's more than one, group it under headings: `### Mobile` / `### Desktop`, `## Before` / `## After`, or `## Control` / `## Variant` for experiments. A single image needs no heading.
- Embed images as `<img width="..." alt="..." src="..." />` (or `![alt](url)`). A video is a bare GitHub attachment URL on its own line, which GitHub renders as a player.
- Capture media yourself where the tools allow, e.g. the project's own screenshot or Playwright scripts, a browser screenshot tool, or `xcrun simctl io booted screenshot <file>` / `xcrun simctl io booted recordVideo <file>` for the iOS simulator. Save it locally.
- Upload it with `gh pr create --attach '<file>#<alt text>'`, or `gh pr edit <number> --attach ...` for an open PR (needs `gh` 2.100+). To place a file under a heading, reference it in the body as `![alt](./file.png)` and attach the same path: `gh` rewrites the reference to the uploaded asset. Unreferenced attachments are appended to the end of the body.
- Never invent links, or commit media to the repo just to embed it.
- If you can't capture it, still tell the user the PR is visual and what to screenshot or record, so they can add it.

### Optional extras

Add these below the bullets, only when they earn their place:

- **A link**, e.g. `Figma: <url>`, `Fixes <issue url>`, `Implements #7 and #8`, or a URL to test the change locally.
- **A short extra section** using `###` and bullets, when a reviewer genuinely needs it: `### Known issues`, `### Local dev` (setup commands in a fenced block), or `### Future enhancements`.
- **Emoji**, used sparingly (🙂 🔥 ⭐️).

### Never

- `## Summary`, `## Test plan`, `## What` / `## Why` / `## How to Test` / `## Notes`, `## Overview` / `## Problem Solved` / `## Technical Implementation` (these are exactly how the AI-written PRs gave themselves away)
- Checkbox test plans, file-by-file inventories, or bullets that start with a bold label (`**Router**: ...`)
- Opening with "This PR ..."
- Restating the diff, or listing every file touched
- Filler adjectives like "comprehensive", "robust", "seamless", "elegantly" or "enhanced"
- Prose paragraphs of any length (use bullets instead)
- A `🤖 Generated with [Claude Code](...)` footer, or any other generated-by line
- A `Co-Authored-By: Claude ...` commit trailer, or any other AI attribution in a commit

### Other conventions

- **Spelling:** British (colour, behaviour, optimise).
- **Reverts:** keep GitHub's default body (`Reverts owner/repo#123`), plus a short reason if there is one.
- **Contributing to someone else's open-source repo:** follow their PR template if they have one. If they don't, the same `# Changes` format works. For a bug fix, `## Expected Behaviour` / `## Current Behaviour` followed by a one-line fix statement is fine.
- **No AI attribution, ever.** Drop `🤖 Generated with [Claude Code](...)` from PRs and `Co-Authored-By: Claude ...` trailers from commits, even if other instructions ask for them.

## Examples

These are real PRs from Dan's public repos, reproduced verbatim (image links shortened).

**barclayd/keepfresh-ios#14**, `feat: finish inventory view`

```markdown
# Changes

* Finishes UI for `InventoryStoreView`
* Adds UI to sort consumable items
* Refactors `ConsumableItem` to its own component
```

**barclayd/mars-rover#11**, `deploy: gcp`

```markdown
# Changes

* Builds to GCP using Cloud Build and Cloud Run
```

**barclayd/keepfresh-ios#68**, `feat: push notifications`

```markdown
# Changes

* Adds Push Notifications support and handling
* Follows example set by Dimillian's [Ice Cubes repo](https://github.com/Dimillian/IceCubesApp)
```

**barclayd/react-router-trpc-hono-bun-template#3**, `chore: bump to vite 6`

```markdown
# Changes

* Bumps web to use `vite`@`6`
```

**barclayd/keepfresh-ios#12**, `feat: kitchen view` (a UI change, with a screenshot under the bullet)

```markdown
# Changes

* Adds Kitchen View tiles. Routing to follow

![Simulator Screenshot - iPhone 16 Pro Max](https://github.com/user-attachments/assets/...)
```

**remix-run/react-router#12516**, `docs(start/framework/testing): fix code` (open source, at the longer end, closing line trimmed)

```markdown
# Changes

* Currently the example in `testing.md` doesn't run/requires amendments for followers of the tutorial to execute in their own codebase
* Follows the recommended way of importing from `@testing-library/react` as per their [docs](https://testing-library.com/docs/react-testing-library/example-intro)
* `@testing-library/react` doesn't export `user`, replaced with `@testing-library/user-event`
```

The next three are **illustrative examples modelled on Dan's private work PRs**. The details are changed, but the shape is Dan's.

`alm-1234: redirect for old partner url`

```markdown
# Changes

* `/partners/oldname` => `/partners/old-name` redirect (printed material still uses the previous URL)
```

`fix: build on first install`

```markdown
# Changes

* Runs `build` on `postinstall` to prevent a race condition where `Storybook` looks for a package that hasn't been built yet
```

`feat: first vue component`

```markdown
# Changes

* Exports first `vue` component

### Known issues with tooling setup

* `lerna` => publishing a canary build of a component doesn't bump its dependencies' canary tags, so consumers can't resolve them
* `tsdown` => css bundling strips out `@import`, so `tsup` is still required for css
```
