"""Protect earlier evidence while permitting new records and metadata corrections."""

import json
import subprocess

import pytest
import yaml

from check_contracts import check_immutable_records


@pytest.fixture
def baseline(tmp_path):
    """Commit small synthetic acquisition and run records as the comparison baseline."""
    acquisition = tmp_path / "data/metadata/acquisitions/example.yaml"
    run = tmp_path / "outputs/runs/example.json"
    acquisition.parent.mkdir(parents=True)
    run.parent.mkdir(parents=True)
    acquisition.write_text(
        yaml.safe_dump(
            {
                "acquisition_id": "example",
                "notes": "Initial metadata",
                "files": [{"path": "raw.csv", "sha256": "a" * 64, "size_bytes": 7}],
            }
        )
    )
    run.write_text(json.dumps({"run_id": "example", "commit": "a" * 40}))
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
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
            "Synthetic evidence baseline",
        ],
        cwd=tmp_path,
        check=True,
    )
    return tmp_path, acquisition, run


@pytest.mark.parametrize("kind", ["acquisition", "run"])
def test_record_deletions_fail(baseline, kind):
    root, acquisition, run = baseline
    (acquisition if kind == "acquisition" else run).unlink()
    with pytest.raises(ValueError, match="Existing record deleted"):
        check_immutable_records(root, "HEAD")


def test_run_edits_fail(baseline):
    root, _, run = baseline
    run.write_text(json.dumps({"run_id": "example", "commit": "b" * 40}))
    with pytest.raises(ValueError, match="Immutable run record changed"):
        check_immutable_records(root, "HEAD")


@pytest.mark.parametrize("change", ["drop_file", "hash", "size", "path"])
def test_file_identity_edits_fail(baseline, change):
    root, acquisition, _ = baseline
    record = yaml.safe_load(acquisition.read_text())
    if change == "drop_file":
        record["files"] = []
    else:
        key, value = {
            "hash": ("sha256", "b" * 64),
            "size": ("size_bytes", 8),
            "path": ("path", "renamed.csv"),
        }[change]
        record["files"][0][key] = value
    acquisition.write_text(yaml.safe_dump(record))
    with pytest.raises(ValueError, match="Immutable file identity changed"):
        check_immutable_records(root, "HEAD")


def test_new_records_and_metadata_corrections_are_allowed(baseline):
    root, acquisition, run = baseline
    record = yaml.safe_load(acquisition.read_text())
    record["notes"] = "Corrected access status, with a reason"
    acquisition.write_text(yaml.safe_dump(record))
    run.with_name("new.json").write_text('{"run_id":"new"}')
    acquisition.with_name("new.yaml").write_text("acquisition_id: new\nfiles: []\n")
    check_immutable_records(root, "HEAD")
