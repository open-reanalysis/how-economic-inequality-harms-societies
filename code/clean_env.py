# SPDX-License-Identifier: MIT
# Purpose: Verify a fresh local clone in the locked environment before release.
# Thread: scaffold
# Reads: committed repository and pixi.lock
# Writes: a temporary clone only
# Network: none for research inputs; environment packages may require download

"""Exercise the committed public replay in a fresh checkout, without copying local inputs."""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from lib.paths import ROOT

if __name__ == "__main__":
    pixi = shutil.which("pixi") or os.environ.get("PIXI_EXE")
    if not pixi:
        raise SystemExit("Put pixi on PATH or set PIXI_EXE to its absolute path")
    with tempfile.TemporaryDirectory(prefix="inequality-replay-") as directory:
        target = Path(directory) / "repo"
        subprocess.run(["git", "clone", "--no-hardlinks", str(ROOT), str(target)], check=True)
        subprocess.run([pixi, "install", "--locked"], cwd=target, check=True)
        subprocess.run(
            ["make", f"PIXI={pixi}", "verify-data", "test", "all"], cwd=target, check=True
        )
