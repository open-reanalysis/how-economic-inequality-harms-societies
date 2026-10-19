# SPDX-License-Identifier: MIT
# Purpose: Reproduce the comparisons selected by a stored analysis specification.
# Thread: scaffold
# Reads: config/specs/, config/results_catalogue.csv, stored inputs and metadata
# Writes: outputs/tables/, outputs/observations/, outputs/runs/
# Network: none

"""Run one specification against verified stored inputs."""

import argparse

from lib.paths import resolve
from lib.pipeline import reproduce

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True)
    args = parser.parse_args()
    reproduce(resolve(args.spec))
