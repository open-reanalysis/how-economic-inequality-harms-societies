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


@pytest.mark.parametrize("credential", ["key", "X-Amz-Signature", "X-Amz-Credential", "sig"])
def test_credentials_are_rejected_before_any_request_or_record(tmp_path, monkeypatch, credential):
    monkeypatch.setenv("OFFLINE", "0")
    with pytest.raises(ValueError, match="Credential-bearing"):
        acquire(
            ["fixture"],
            f"https://example.invalid/?{credential}=synthetic-fixture",
            "raw.csv",
            redistributable=True,
            root=tmp_path,
        )
    assert not list(tmp_path.iterdir())


@pytest.mark.parametrize("failure", ["http", "connection", "read"])
def test_redirect_secrets_never_enter_failure_records(tmp_path, monkeypatch, failure):
    import requests

    monkeypatch.setenv("OFFLINE", "0")
    secret = "SYNTHETIC-SIGNED-URL-SECRET"
    signed = "https://example.invalid/blob?X-Amz-Signature=" + secret

    class Response:
        status_code = 403 if failure == "http" else 200
        url = signed

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def raise_for_status(self):
            if failure == "http":
                raise requests.HTTPError("403 for url: " + signed)

        def iter_content(self, size):
            raise requests.ConnectionError("read failed: " + signed)

    def request(*args, **kwargs):
        if failure == "connection":
            raise requests.ConnectionError("connect failed: " + signed)
        return Response()

    monkeypatch.setattr("lib.download.requests.get", request)
    record = acquire(
        ["fixture"],
        "https://example.invalid/public",
        "raw.csv",
        redistributable=True,
        root=tmp_path,
    )
    assert record["status"] == "access_failed"
    assert secret not in json.dumps(record)
    assert "resolved_url" not in record
    for path in tmp_path.rglob("*.yaml"):
        assert secret not in path.read_text()


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
    producer = {
        "spec_sha256": "spec",
        "input_hashes": {"raw": "input"},
        "code_sha256": "code",
        "pixi_lock_sha256": "env",
    }
    assert can_retain(producer, "spec", {"raw": "input"}, "code", "env")
    assert not can_retain(producer, "new-spec", {"raw": "input"}, "code", "env")
    assert not can_retain(producer, "spec", {"raw": "input"}, "new-code", "env")
    assert not can_retain(producer, "spec", {"raw": "changed"}, "code", "env")

    assert not can_retain(producer, "spec", {"raw": "input"}, "code", "new-env")


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
