#!/bin/sh
set -eu

codex_dir=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
bin_dir="${TESTFLIGHT_BIN_DIR:-$HOME/.local/bin}"
skill_dir="${CODEX_HOME:-$HOME/.codex}/skills"

check_link() {
    if [ -L "$2" ] && [ "$(readlink "$2")" = "$1" ]; then return; fi
    if [ -e "$2" ] || [ -L "$2" ]; then
        printf 'Destination already exists; leaving it untouched: %s\n' "$2" >&2
        exit 1
    fi
}

check_link "$codex_dir/scripts/testflight.py" "$bin_dir/testflight"
check_link "$codex_dir/skills/testflight-release" "$skill_dir/testflight-release"
python3 -c 'import sys; assert sys.version_info >= (3, 11), "Python 3.11+ is required"'
if ! command -v asc >/dev/null 2>&1; then
    printf 'Install ASC first: brew install asc\n' >&2
    exit 1
fi
mkdir -p "$bin_dir" "$skill_dir"
[ -L "$bin_dir/testflight" ] || ln -s "$codex_dir/scripts/testflight.py" "$bin_dir/testflight"
[ -L "$skill_dir/testflight-release" ] || ln -s "$codex_dir/skills/testflight-release" "$skill_dir/testflight-release"
printf 'Installed testflight and testflight-release. Run testflight --help.\n'
