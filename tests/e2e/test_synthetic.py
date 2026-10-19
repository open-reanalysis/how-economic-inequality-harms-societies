"""Synthetic country and state paths through validation, preparation and computation."""

import pandas as pd
import pytest

from lib.compute import correlation
from lib.schemas import validate_observations, validate_result_keys
from lib.transform import prepare


@pytest.mark.parametrize(
    "dataset,kind,units",
    [
        ("international", "country", ["AAA", "BBB", "CCC", "DDD"]),
        ("us_states", "us_state", ["01", "02", "04", "05"]),
    ],
)
def test_three_variants_have_distinct_identity_and_observation_paths(
    dataset, kind, units, tmp_path
):
    rows = []
    for variable, values in [("x", [1.0, 2.0, 3.0, 4.0]), ("y", [1.0, 3.0, 2.0, 4.0])]:
        for unit, value in zip(units, values):
            rows.append(
                dict(
                    dataset=dataset,
                    unit_type=kind,
                    unit_id=unit,
                    variable_id=variable,
                    period="2000",
                    value=value,
                    unit="score",
                    source_id="synthetic",
                    file_path="synthetic.csv",
                    provenance="released",
                )
            )
    raw = tmp_path / "synthetic.csv"
    pd.DataFrame(rows).to_csv(raw, index=False)
    stored = pd.read_csv(raw, dtype={"unit_id": str, "period": str})
    registries = {
        "international": set(units) if dataset == "international" else set(),
        "us_states": set(units) if dataset == "us_states" else set(),
    }
    checked = validate_observations(stored, registries)
    spec = {
        "dataset": dataset,
        "variables": [
            {
                "variable_id": variable,
                "period": "2000",
                "unit": "score",
                "sources": ["synthetic"],
                "transformation": "none",
                "direction": "as_is",
            }
            for variable in ["x", "y"]
        ],
    }
    keys = []
    paths = set()
    for variant in ["updated", "refreshed", "with_substitutes"]:
        # Synthetic arithmetic exercises variants without running current research data.
        result = correlation(prepare(checked, spec, units), "x", "y")
        assert result["r"] == pytest.approx(0.8) and result["n"] == 4
        path = tmp_path / dataset / variant / "example.csv"
        path.parent.mkdir(parents=True)
        result["observations"].to_csv(path)
        paths.add(path)
        keys.append(dict(spec_id=dataset, spec_version=1, result_id="example", variant_id=variant))
    validate_result_keys(pd.DataFrame(keys))
    assert len(paths) == 3
    assert correlation(prepare(checked, spec, units), "x", "absent")["reason"].startswith("Missing")
