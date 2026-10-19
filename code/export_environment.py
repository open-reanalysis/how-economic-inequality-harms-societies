# SPDX-License-Identifier: MIT
# Purpose: Export deterministic informational environment views from the Pixi lock.
# Thread: scaffold
# Reads: pixi.toml and pixi.lock through the Pixi CLI
# Writes: environment.yml and requirements.txt, or verifies them with --check
# Network: none

"""Export the Linux lock view; Pixi remains the authoritative cross-platform installer."""

import argparse
import json
import os
import shutil
import subprocess

from lib.paths import ROOT

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    executable = shutil.which("pixi") or os.environ.get("PIXI_EXE")
    if not executable:
        raise SystemExit("Set PIXI_EXE or put pixi on PATH")
    environment = subprocess.check_output(
        [
            executable,
            "workspace",
            "export",
            "conda-environment",
            "--from-lock-file",
            "--platform",
            "linux-64",
        ],
        cwd=ROOT,
        text=True,
    )
    environment = environment.rstrip() + "\n"
    packages = json.loads(
        subprocess.check_output(
            [executable, "list", "--json", "--locked", "--platform", "linux-64"],
            cwd=ROOT,
            text=True,
        )
    )
    requirements = "# Informational direct Python dependencies from pixi.lock (linux-64).\n# Install with pixi install --locked; this is not a replacement lockfile.\n"
    requirements += "".join(
        f"{p['name']}=={p['version']}\n"
        for p in sorted(packages, key=lambda x: x["name"])
        if p["is_explicit"] and p["name"] != "python"
    )
    for name, text in [("environment.yml", environment), ("requirements.txt", requirements)]:
        path = ROOT / name
        if args.check:
            if not path.exists() or path.read_text() != text:
                raise SystemExit(f"Stale environment export: {name}")
        else:
            path.write_text(text)
