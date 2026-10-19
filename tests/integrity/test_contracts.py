"""Source integrity, replay gates and retained-output compatibility."""

import json

import pandas as pd
import pytest

from lib.download import acquire
from lib.paths import resolve
from lib.records import verify_files
from lib.runs import can_retain
from lib.schemas import validate_observations, validate_result_keys
from lib.spec import require_current_gate


def test_download_refuses_network_offline(tmp_path):
    with pytest.raises(RuntimeError, match="offline"):
        acquire(
            ["fixture"], "https://example.invalid/", "raw.csv", redistributable=True, root=tmp_path
        )


def test_restricted_input_may_be_missing_but_public_input_must_exist(tmp_path):
    file = {"path": "raw.csv", "storage": "local", "size_bytes": 0, "sha256": "0" * 64}
    assert verify_files([{"files": [file]}], tmp_path) == ["raw.csv"]
    file["storage"] = "git"
    with pytest.raises(ValueError, match="Missing published"):
        verify_files([{"files": [file]}], tmp_path)


def test_tampered_file_fails(tmp_path):
    (tmp_path / "raw.csv").write_text("changed")
    file = {"path": "raw.csv", "storage": "git", "size_bytes": 7, "sha256": "0" * 64}
    with pytest.raises(ValueError, match="checksum"):
        verify_files([{"files": [file]}], tmp_path)


def test_retention_requires_code_spec_and_input_identity():
    producer = {"spec_sha256": "spec", "input_hashes": {"raw": "input"}, "code_sha256": "code"}
    assert can_retain(producer, "spec", {"raw": "input"}, "code")
    assert not can_retain(producer, "new-spec", {"raw": "input"}, "code")
    assert not can_retain(producer, "spec", {"raw": "input"}, "new-code")
    assert not can_retain(producer, "spec", {"raw": "changed"}, "code")


def test_current_gate_rejects_draft_lock(tmp_path):
    (tmp_path / "config").mkdir()
    (tmp_path / "config/reproduction_lock.yaml").write_text("status: draft\n")
    with pytest.raises(PermissionError, match="not approved"):
        require_current_gate(tmp_path / "config/specs/updated.yaml", tmp_path)


def test_paths_cannot_escape_repository(tmp_path):
    with pytest.raises(ValueError, match="escapes"):
        resolve("../elsewhere", tmp_path)


def test_duplicate_variant_result_keys_fail():
    frame = pd.DataFrame(
        [{"spec_id": "test", "spec_version": 1, "result_id": "x", "variant_id": "updated"}] * 2
    )
    with pytest.raises(ValueError, match="Duplicate result"):
        validate_result_keys(frame)


def test_unknown_unit_and_wrong_unit_type_fail():
    row = dict(
        dataset="us_states",
        unit_type="us_state",
        unit_id="01",
        variable_id="x",
        period="2000",
        value=1.0,
        unit="years",
        source_id="fixture",
        file_path="fixture.csv",
        provenance="released",
    )
    registries = {"us_states": {"01"}, "international": {"USA"}}
    validate_observations(pd.DataFrame([row]), registries)
    row["unit_id"] = "99"
    with pytest.raises(ValueError, match="Unknown units"):
        validate_observations(pd.DataFrame([row]), registries)
    row.update(unit_id="01", unit_type="country")
    with pytest.raises(ValueError, match="Unit type"):
        validate_observations(pd.DataFrame([row]), registries)


def test_raw_caption_and_csv_hashes_match():
    from lib.paths import ROOT, sha256

    folder = ROOT / "sources/supporting/original-authors/wilkinson-2011-ted"
    for name, expected in json.loads((folder / "source.json").read_text())["sha256"].items():
        assert sha256(folder / name) == expected
