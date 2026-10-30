# Claude Code Setup

## Skills

Symlink each skill into `~/.claude/skills` so Claude Code picks it up across every project:

```shell
mkdir -p ~/.claude/skills
ln -s ~/<PATH_TO_THIS_REPO>/claude/skills/pr-and-commit-style ~/.claude/skills/pr-and-commit-style
ln -s ~/<PATH_TO_THIS_REPO>/claude/skills/iphone-duo-design ~/.claude/skills/iphone-duo-design
```

* `pr-and-commit-style` => commit messages, branch names, PR titles and PR descriptions in my style (distilled from my PRs and commits before AI started writing them)
* `iphone-duo-design` => designing and adapting iOS apps for iPhone Duo (the rail, side-by-side panes, tent mode, reserved regions, mock-ups and SwiftUI pitfalls), from Apple's HIG, docs and tech talks plus lessons from building on a real device
