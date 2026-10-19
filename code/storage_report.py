# SPDX-License-Identifier: MIT
# Purpose: Report recorded data sizes and packed Git history without changing storage.
# Thread: scaffold
# Reads: data/metadata/acquisitions/ and git object statistics
# Writes: none
# Network: none

"""Display storage sizes and review thresholds."""

import subprocess

from lib.records import load_records

if __name__ == "__main__":
    _, acquisitions = load_records()
    total = sum(file["size_bytes"] for record in acquisitions for file in record["files"])
    print(f"Recorded raw files: {total} bytes; data review threshold: {500 * 1024**2} bytes")
    print(subprocess.check_output(["git", "count-objects", "-v"], text=True))
