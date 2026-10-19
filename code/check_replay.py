# SPDX-License-Identifier: MIT
# Purpose: Compare replayed tables with committed snapshots at declared numerical tolerances.
# Thread: scaffold
# Reads: outputs/tables/ and the selected Git revision
# Writes: none
# Network: none

"""Keep identifiers and metadata exact while allowing documented floating-point variation."""

import argparse
import io
import subprocess

import numpy as np
import pandas as pd

from lib.paths import ROOT


def compare(expected: pd.DataFrame, actual: pd.DataFrame) -> None:
    """Require equal row identities, metadata, missingness and admissible numeric differences."""
    if list(expected.columns) != list(actual.columns) or len(expected) != len(actual):
        raise ValueError("Replay table shape or columns changed")
    keys = [
        c
        for c in [
            "result_id",
            "variant_id",
            "spec_id",
            "spec_version",
            "dataset",
            "unit_id",
            "variable_id",
            "component",
            "source_id",
            "period",
        ]
        if c in expected
    ]
    if keys:
        expected = expected.sort_values(keys).reset_index(drop=True)
        actual = actual.sort_values(keys).reset_index(drop=True)
    for column in expected:
        if column in {"r", "p", "z_score", "index_value"}:
            left = pd.to_numeric(expected[column].mask(expected[column].eq(""), np.nan))
            right = pd.to_numeric(actual[column].mask(actual[column].eq(""), np.nan))
            if not left.isna().equals(right.isna()):
                raise ValueError(f"Replay missingness changed: {column}")
            relative = 1e-8 if column == "p" else 0
            absolute = 0 if column == "p" else 1e-10
            if not np.allclose(left, right, rtol=relative, atol=absolute, equal_nan=True):
                raise ValueError(f"Replay numeric tolerance exceeded: {column}")
        elif not expected[column].equals(actual[column]):
            raise ValueError(f"Replay identity or metadata changed: {column}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="HEAD")
    args = parser.parse_args()
    count = 0
    for path in sorted((ROOT / "outputs/tables").glob("*.csv")):
        name = str(path.relative_to(ROOT))
        committed = subprocess.run(
            ["git", "show", f"{args.base}:{name}"], cwd=ROOT, capture_output=True, text=True
        )
        if committed.returncode:
            raise SystemExit(f"Replay output lacks a committed snapshot: {name}")
        expected = pd.read_csv(io.StringIO(committed.stdout), dtype=str, keep_default_na=False)
        actual = pd.read_csv(path, dtype=str, keep_default_na=False)
        compare(expected, actual)
        count += 1
    print(f"Replay: {count} tables match, with exact metadata and declared numerical tolerances.")
