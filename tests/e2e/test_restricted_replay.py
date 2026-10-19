"""Exercise the actual stored-input pipeline and restricted-input retention path."""

import csv
import json
import subprocess

import pandas as pd
import yaml

from lib.paths import sha256
from lib.pipeline import reproduce


def test_real_pipeline_retains_only_compatible_produced_result(tmp_path):
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
        redistributable=False,
    )
    (root / "data/metadata/sources/fixture.yaml").write_text(yaml.safe_dump(source))
    file = dict(
        path="raw.csv",
        size_bytes=raw.stat().st_size,
        sha256=sha256(raw),
        storage="local",
        redistributable=False,
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
    incompatible_record = reproduce(spec_path, root)
    assert json.loads((root / incompatible_record).read_text())["steps"][0]["state"] == "computed"
    assert pd.read_csv(output).iloc[0].state == "not_produced"
