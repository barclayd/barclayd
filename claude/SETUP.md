# Claude Code Setup

## Skills

Symlink each skill into `~/.claude/skills` so Claude Code picks it up across every project:

```shell
mkdir -p ~/.claude/skills
ln -s ~/<PATH_TO_THIS_REPO>/claude/skills/pr-and-commit-style ~/.claude/skills/pr-and-commit-style
```

* `pr-and-commit-style` => commit messages, branch names, PR titles and PR descriptions in my style (distilled from my PRs and commits before AI started writing them)
