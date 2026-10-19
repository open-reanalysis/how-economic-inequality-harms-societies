"""Replay accepts floating-point noise, never sample or result-identity changes."""

import subprocess

import pandas as pd
import pytest

from check_replay import check_tables, compare


def test_numeric_tolerance_keeps_metadata_and_missingness_exact():
    expected = pd.DataFrame(
        [{"result_id": "example", "variant_id": "historical", "r": "0.8", "p": "0.2", "n": "4"}]
    )
    actual = expected.copy()
    actual.loc[0, "r"] = "0.800000000001"
    compare(expected, actual)
    actual.loc[0, "n"] = "3"
    with pytest.raises(ValueError, match="metadata"):
        compare(expected, actual)
    actual = expected.copy()
    actual.loc[0, "r"] = ""
    with pytest.raises(ValueError, match="missingness"):
        compare(expected, actual)
    actual = expected.copy()
    actual.loc[0, "p"] = "0.201"
    with pytest.raises(ValueError, match="tolerance"):
        compare(expected, actual)


@pytest.mark.parametrize("change", ["none", "missing", "extra", "empty_baseline"])
def test_replay_requires_the_complete_committed_file_set(tmp_path, change):
    folder = tmp_path / "outputs/tables"
    folder.mkdir(parents=True)
    table = folder / "result.csv"
    table.write_text("result_id,r\nexample,0.8\n")
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    if change == "empty_baseline":
        table.unlink()
        (tmp_path / "README.md").write_text("Synthetic empty baseline")
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.name=Fixture",
            "-c",
            "user.email=fixture@example.invalid",
            "commit",
            "-qm",
            "Synthetic replay baseline",
        ],
        cwd=tmp_path,
        check=True,
    )
    if change == "missing":
        table.unlink()
    elif change == "extra":
        (folder / "unexpected.csv").write_text(table.read_text())
    if change == "none":
        assert check_tables("HEAD", tmp_path) == 1
    else:
        with pytest.raises(ValueError, match="paths changed|no committed result"):
            check_tables("HEAD", tmp_path)


def test_coverage_replay_distinguishes_master_samples_after_row_shuffle():
    expected = pd.DataFrame(
        {
            "dataset": ["international", "international"],
            "sample": ["historical", "refreshed"],
            "unit_id": ["AUT", "AUT"],
            "component": ["trust", "trust"],
            "candidate_has_observation": ["True", "True"],
        }
    )
    compare(expected, expected.iloc[::-1].reset_index(drop=True))
    changed = expected.copy()
    changed.loc[1, "sample"] = "different_sample"
    with pytest.raises(ValueError, match="identity or metadata"):
        compare(expected, changed)
