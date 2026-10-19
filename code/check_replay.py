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


def check_tables(base: str, root=ROOT) -> int:
    """Compare the complete expected CSV path set and every table's contents."""
    expected_paths = {
        name
        for name in subprocess.check_output(
            ["git", "ls-tree", "-r", "--name-only", base, "--", "outputs/tables"],
            cwd=root,
            text=True,
        ).splitlines()
        if name.endswith(".csv") and name.count("/") == 2
    }
    actual_paths = {str(path.relative_to(root)) for path in (root / "outputs/tables").glob("*.csv")}
    if expected_paths != actual_paths:
        raise ValueError(
            f"Replay output paths changed: missing={sorted(expected_paths - actual_paths)}, "
            f"unexpected={sorted(actual_paths - expected_paths)}"
        )
    if not expected_paths:
        raise ValueError("Replay has no committed result tables to compare")
    for name in sorted(expected_paths):
        committed = subprocess.check_output(["git", "show", f"{base}:{name}"], cwd=root, text=True)
        expected = pd.read_csv(io.StringIO(committed), dtype=str, keep_default_na=False)
        actual = pd.read_csv(root / name, dtype=str, keep_default_na=False)
        compare(expected, actual)
    return len(expected_paths)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="HEAD")
    args = parser.parse_args()
    count = check_tables(args.base)
    print(f"Replay: {count} tables match, with exact metadata and declared numerical tolerances.")
