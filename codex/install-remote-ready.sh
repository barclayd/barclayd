#!/bin/sh
set -eu

codex_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
bin_dir="${REMOTE_READY_BIN_DIR:-$HOME/.local/bin}"
skill_dir="${CODEX_HOME:-$HOME/.codex}/skills"

check_link() {
    if [ -L "$2" ] && [ "$(readlink "$2")" = "$1" ]; then
        return
    fi
    if [ -e "$2" ] || [ -L "$2" ]; then
        printf 'Destination already exists; leaving it untouched: %s\n' "$2" >&2
        exit 1
    fi
}

check_link "$codex_dir/scripts/remote_ready.py" "$bin_dir/remote-ready"
check_link "$codex_dir/skills/remote-ready" "$skill_dir/remote-ready"
python3 -c 'import sys; assert sys.version_info >= (3, 11), "Python 3.11+ is required"'
mkdir -p "$bin_dir" "$skill_dir"
[ -L "$bin_dir/remote-ready" ] || ln -s "$codex_dir/scripts/remote_ready.py" "$bin_dir/remote-ready"
[ -L "$skill_dir/remote-ready" ] || ln -s "$codex_dir/skills/remote-ready" "$skill_dir/remote-ready"
printf 'Installed %s and %s\n' "$bin_dir/remote-ready" "$skill_dir/remote-ready"
printf 'Ensure %s is on PATH. Run remote-ready --help for options.\n' "$bin_dir"
