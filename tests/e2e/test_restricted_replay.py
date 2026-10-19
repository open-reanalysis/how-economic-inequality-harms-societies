"""Exercise the actual stored-input pipeline and restricted-input retention path."""

import csv
import json
import subprocess

import pandas as pd
import pytest
import yaml

from lib.coverage import build_coverage
from lib.paths import sha256
from lib.pipeline import reproduce


def create_case(tmp_path, *, public=False):
    """Build a stored-input case with an independent known correlation."""
    root = tmp_path
    for directory in [
        "code",
        "config/specs",
        "config/units",
        "data/metadata/sources",
        "data/metadata/acquisitions",
        "docs",
        "outputs/runs",
    ]:
        (root / directory).mkdir(parents=True)
    (root / "pixi.lock").write_text("synthetic test environment identity")
    (root / "code/core.py").write_text("# Synthetic code identity, not imported\n")
    (root / "config/units/countries.csv").write_text(
        "unit_id,name,aliases\nAAA,A,\nBBB,B,\nCCC,C,\nDDD,D,\n"
    )
    (root / "config/units/us_states.csv").write_text("unit_id,name,aliases\n01,Alabama,\n")
    rows = []
    for variable, values in [("x", [1.0, 2.0, 3.0, 4.0]), ("y", [1.0, 3.0, 2.0, 4.0])]:
        for unit, value in zip(["AAA", "BBB", "CCC", "DDD"], values):
            rows.append(
                dict(
                    dataset="international",
                    unit_type="country",
                    unit_id=unit,
                    variable_id=variable,
                    period="2000",
                    value=value,
                    unit="score",
                    source_id="fixture",
                    file_path="raw.csv",
                    provenance="released",
                )
            )
    raw = root / "raw.csv"
    pd.DataFrame(rows).to_csv(raw, index=False)
    source = dict(
        source_id="fixture",
        provider="Synthetic",
        series_code="synthetic",
        title="Synthetic",
        definition="Synthetic",
        unit="score",
        geography="countries",
        licence="Test fixture",
        terms_url="https://example.invalid/",
        redistributable=public,
    )
    (root / "data/metadata/sources/fixture.yaml").write_text(yaml.safe_dump(source))
    file = dict(
        path="raw.csv",
        size_bytes=raw.stat().st_size,
        sha256=sha256(raw),
        storage="git" if public else "local",
        redistributable=public,
        source_ids=["fixture"],
    )
    acquisition = dict(
        acquisition_id="fixture-acq",
        source_ids=["fixture"],
        status="acquired",
        retrieval_log="docs/retrieval.txt",
        files=[file],
    )
    (root / "docs/retrieval.txt").write_text("Synthetic fixture created inside the test.")
    (root / "data/metadata/acquisitions/fixture-acq.yaml").write_text(yaml.safe_dump(acquisition))
    spec = dict(
        spec_id="historical_international",
        version=1,
        dataset="international",
        unit_type="country",
        catalogue="config/results_catalogue.csv",
        samples={"historical": {"units": ["AAA", "BBB", "CCC", "DDD"]}},
        variables=[
            dict(
                variable_id=v,
                sources=["fixture"],
                period="2000",
                unit="score",
                conversion="none",
                transformation="none",
                direction="as_is",
                rationale="synthetic",
            )
            for v in ["x", "y"]
        ],
        index={"mode": "supplied"},
        statistics=["pearson_r", "p_value", "n"],
        inputs=[dict(path="raw.csv", source_id="fixture", reader="long_csv")],
        data_provenance="released",
        access_label="DIRECT REPRODUCTION",
        method_deviations="",
    )
    spec_path = root / "config/specs/historical_international.yaml"
    spec_path.write_text(yaml.safe_dump(spec))
    with (root / "config/results_catalogue.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(
            stream, fieldnames=["result_id", "dataset", "predictor", "indicator_or_index"]
        )
        writer.writeheader()
        writer.writerow(
            dict(
                result_id="example", dataset="international", predictor="x", indicator_or_index="y"
            )
        )
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.name=Fixture",
            "-c",
            "user.email=fixture@example.invalid",
            "commit",
            "-qm",
            "Synthetic fixture",
        ],
        cwd=root,
        check=True,
    )
    return spec_path, raw


def test_real_pipeline_retains_only_compatible_produced_result(tmp_path):
    root = tmp_path
    spec_path, raw = create_case(root)
    produced_record = reproduce(spec_path, root)
    output = root / "outputs/tables/historical_international_results.csv"
    before = output.read_bytes()
    assert pd.read_csv(output).iloc[0].r == 0.8
    assert not (root / "outputs/observations").exists()
    raw.unlink()
    retained_record = reproduce(spec_path, root)
    retained = json.loads((root / retained_record).read_text())
    assert retained["steps"][0]["state"] == "retained"
    assert (
        retained["steps"][0]["producer_run"]
        == json.loads((root / produced_record).read_text())["run_id"]
    )
    assert output.read_bytes() == before
    (root / "code/core.py").write_text("# Changed computation identity\n")
    with pytest.raises(ValueError, match="No compatible producer"):
        reproduce(spec_path, root)
    assert output.read_bytes() == before


def test_changed_environment_cannot_retain_old_results(tmp_path):
    spec_path, raw = create_case(tmp_path)
    reproduce(spec_path, tmp_path)
    output = tmp_path / "outputs/tables/historical_international_results.csv"
    before = output.read_bytes()
    raw.unlink()
    (tmp_path / "pixi.lock").write_text("Changed numerical dependency environment")
    with pytest.raises(ValueError, match="No compatible producer"):
        reproduce(spec_path, tmp_path)
    assert output.read_bytes() == before


@pytest.mark.parametrize("barrier", ["missing_variable", "restriction"])
def test_obsolete_observations_and_figures_are_removed(tmp_path, barrier):
    spec_path, _ = create_case(tmp_path, public=True)
    reproduce(spec_path, tmp_path)
    observations = tmp_path / "outputs/observations/historical_international/historical/example.csv"
    figure = tmp_path / "outputs/figures/historical_international/historical/example.png"
    assert observations.is_file() and figure.is_file()
    if barrier == "missing_variable":
        spec = yaml.safe_load(spec_path.read_text())
        spec["variables"][1]["status"] = "UNRESOLVED"
        spec_path.write_text(yaml.safe_dump(spec))
    else:
        record_path = tmp_path / "data/metadata/acquisitions/fixture-acq.yaml"
        record = yaml.safe_load(record_path.read_text())
        record["files"][0].update(redistributable=False, storage="local")
        record_path.write_text(yaml.safe_dump(record))
    reproduce(spec_path, tmp_path)
    assert not observations.exists() and not figure.exists()
    result = pd.read_csv(tmp_path / "outputs/tables/historical_international_results.csv").iloc[0]
    assert result.state == ("not_produced" if barrier == "missing_variable" else "computed")


@pytest.mark.parametrize("signal", ["declared_current", "current_rows", "current_path", "unknown"])
def test_current_inputs_cannot_enter_historical_reproduction(tmp_path, monkeypatch, signal):
    spec_path, raw = create_case(tmp_path)
    (tmp_path / "config/reproduction_lock.yaml").write_text("status: draft\n")
    spec = yaml.safe_load(spec_path.read_text())
    if signal == "declared_current":
        spec["data_provenance"] = "current"
    elif signal == "unknown":
        spec.pop("data_provenance")
        spec["spec_id"] = "another_name"
    elif signal == "current_path":
        spec["inputs"][0]["path"] = "data/01_raw_current/example.csv"
    else:
        frame = pd.read_csv(raw)
        frame["provenance"] = "current"
        frame.to_csv(raw, index=False)
        path = tmp_path / "data/metadata/acquisitions/fixture-acq.yaml"
        record = yaml.safe_load(path.read_text())
        record["files"][0].update(sha256=sha256(raw), size_bytes=raw.stat().st_size)
        path.write_text(yaml.safe_dump(record))
    spec_path.write_text(yaml.safe_dump(spec))

    def forbidden(*args, **kwargs):
        raise AssertionError("The current gate must run before correlation")

    monkeypatch.setattr("lib.pipeline.compute.correlation", forbidden)
    with pytest.raises(PermissionError, match="not approved"):
        reproduce(spec_path, tmp_path)
    assert not list((tmp_path / "outputs/runs").glob("*.json"))


@pytest.mark.parametrize(
    "values,missing,n", [([1.0, 1.0, 1.0, 1.0], "", 4), ([1.0, 2.0, None, None], "CCC;DDD", 2)]
)
def test_uncomputable_comparison_preserves_observed_membership(tmp_path, values, missing, n):
    spec_path, raw = create_case(tmp_path)
    frame = pd.read_csv(raw)
    frame.loc[frame.variable_id.eq("y"), "value"] = [
        float("nan") if value is None else value for value in values
    ]
    frame.to_csv(raw, index=False)
    path = tmp_path / "data/metadata/acquisitions/fixture-acq.yaml"
    record = yaml.safe_load(path.read_text())
    record["files"][0].update(sha256=sha256(raw), size_bytes=raw.stat().st_size)
    path.write_text(yaml.safe_dump(record))
    reproduce(spec_path, tmp_path)
    result = pd.read_csv(
        tmp_path / "outputs/tables/historical_international_results.csv", keep_default_na=False
    ).iloc[0]
    assert result.state == "not_produced" and result.n == n
    assert result.missing_units == missing


def test_restricted_current_coverage_needs_compatible_producer(tmp_path):
    _, old_raw = create_case(tmp_path)
    path = tmp_path / "data/01_raw_current/local/who.json"
    path.parent.mkdir(parents=True)
    path.write_text(
        json.dumps(
            dict(value=[dict(SpatialDim="AAA", TimeDim=2024, Dim1="SEX_BTSX", NumericValue=1)])
        )
    )
    old_raw.unlink()
    source_path = tmp_path / "data/metadata/sources/fixture.yaml"
    source = yaml.safe_load(source_path.read_text())
    source.update(coverage_format="who_odata", coverage_filters=dict(Dim1="SEX_BTSX"))
    source_path.write_text(yaml.safe_dump(source))
    acquisition_path = tmp_path / "data/metadata/acquisitions/fixture-acq.yaml"
    record = yaml.safe_load(acquisition_path.read_text())
    record["files"][0].update(
        path=str(path.relative_to(tmp_path)), sha256=sha256(path), size_bytes=path.stat().st_size
    )
    acquisition_path.write_text(yaml.safe_dump(record))
    produced = build_coverage(tmp_path)
    output = tmp_path / "outputs/tables/outcome_source_coverage.csv"
    expected = output.read_bytes()
    path.unlink()
    retained = build_coverage(tmp_path)
    step = json.loads((tmp_path / retained).read_text())["steps"][0]
    assert step["state"] == "retained"
    assert step["producer_run"] == json.loads((tmp_path / produced).read_text())["run_id"]
    (tmp_path / "pixi.lock").write_text("changed environment")
    with pytest.raises(ValueError, match="No compatible producer"):
        build_coverage(tmp_path)
    assert output.read_bytes() == expected
