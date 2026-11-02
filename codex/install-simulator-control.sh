#!/bin/sh
set -eu

codex_dir=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
bin_dir="${SIMULATOR_CONTROL_BIN_DIR:-$HOME/.local/bin}"
skill_dir="${CODEX_HOME:-$HOME/.codex}/skills"
duoctl="$codex_dir/skills/simulator-control/vendor/duoctl/duoctl"

check_link() {
    if [ -L "$2" ] && [ "$(readlink "$2")" = "$1" ]; then return; fi
    if [ -e "$2" ] || [ -L "$2" ]; then
        printf 'Destination already exists; leaving it untouched: %s\n' "$2" >&2
        exit 1
    fi
}

check_link "$duoctl" "$bin_dir/duoctl"
check_link "$codex_dir/skills/simulator-control" "$skill_dir/simulator-control"
mkdir -p "$bin_dir" "$skill_dir"
[ -L "$bin_dir/duoctl" ] || ln -s "$duoctl" "$bin_dir/duoctl"
[ -L "$skill_dir/simulator-control" ] || ln -s "$codex_dir/skills/simulator-control" "$skill_dir/simulator-control"
printf 'Installed duoctl and simulator-control.\n'
command -v axe >/dev/null 2>&1 || printf 'Install AXe too: brew install cameroncooke/axe/axe\n'
