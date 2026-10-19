# SPDX-License-Identifier: MIT
# Purpose: Summarise nonmissing flags and payload validity without exposing current values.
# Thread: outcome-data
# Reads: data/metadata/ and stored candidate current responses
# Writes: outputs/tables/outcome_source_coverage.csv and outputs/runs/
# Network: none

"""Inspect source coverage only; never calculate current associations."""

from lib.coverage import build_coverage

if __name__ == "__main__":
    print(build_coverage())
