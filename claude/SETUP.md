# Claude Code Setup

## Skills

Symlink the whole skills folder into `~/.claude/skills` so Claude Code picks up every skill in this repo across every project, including new ones as they're added:

```shell
# move any existing skills into the repo first, then remove the folder
mv ~/.claude/skills/* ~/<PATH_TO_THIS_REPO>/claude/skills/
rmdir ~/.claude/skills
ln -s ~/<PATH_TO_THIS_REPO>/claude/skills ~/.claude/skills
```

Claude Code writes its own synced skills to `skills/synced/` and `skills/.trash/`, both gitignored.

* `pr-and-commit-style` => commit messages, branch names, PR titles and PR descriptions in my style (distilled from my PRs and commits before AI started writing them)
