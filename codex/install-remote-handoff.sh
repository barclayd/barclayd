#!/bin/sh
set -eu

codex_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
skill_dir="${CODEX_HOME:-$HOME/.codex}/skills"
source_dir="$codex_dir/skills/remote-handoff"
destination="$skill_dir/remote-handoff"

if [ -L "$destination" ] && [ "$(readlink "$destination")" = "$source_dir" ]; then
    printf 'Already installed: %s\n' "$destination"
    exit 0
fi
if [ -e "$destination" ] || [ -L "$destination" ]; then
    printf 'Destination already exists; leaving it untouched: %s\n' "$destination" >&2
    exit 1
fi

mkdir -p "$skill_dir"
ln -s "$source_dir" "$destination"
printf 'Installed %s\n' "$destination"
