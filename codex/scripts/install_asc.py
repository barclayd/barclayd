#!/usr/bin/env python3
"""Install the checksum-pinned macOS ASC binary into an explicitly chosen directory."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import tempfile
import urllib.request


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bin-dir", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads((Path(__file__).resolve().parents[1] / "testflight-toolchain.json").read_text())
    arch = {"arm64": "arm64", "aarch64": "arm64", "x86_64": "amd64"}.get(platform.machine())
    if platform.system() != "Darwin" or arch is None:
        parser.error("This installer supports macOS arm64 and amd64 only.")
    version = config["asc_version"]
    expected = config[f"macOS_{arch}_sha256"]
    destination = args.bin_dir / "asc"
    args.bin_dir.mkdir(parents=True, exist_ok=True)
    if destination.exists() or destination.is_symlink():
        if destination.is_file() and hashlib.sha256(destination.read_bytes()).hexdigest() == expected:
            print(f"ASC {version} already installed.")
            return
        parser.error("Destination exists and differs from the pinned binary; left unchanged.")
    url = f"https://github.com/rorkai/App-Store-Connect-CLI/releases/download/{version}/asc_{version}_macOS_{arch}"
    with urllib.request.urlopen(url, timeout=120) as response:
        binary = response.read()
    if hashlib.sha256(binary).hexdigest() != expected:
        parser.error("Downloaded ASC checksum does not match; nothing was installed.")
    fd, temp = tempfile.mkstemp(dir=args.bin_dir, prefix=".asc-")
    try:
        with os.fdopen(fd, "wb") as file:
            file.write(binary)
        os.chmod(temp, 0o755)
        os.link(temp, destination)
    finally:
        os.unlink(temp)
    print(f"Installed ASC {version} at {destination}")


if __name__ == "__main__":
    main()
