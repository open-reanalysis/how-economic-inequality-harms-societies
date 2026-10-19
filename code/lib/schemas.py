"""Canonical interface schemas and semantic integrity checks."""

import numpy as np
import pandas as pd
import pandera.pandas as pa

OBSERVATION_KEY = ["dataset", "unit_id", "variable_id", "period", "source_id"]
OBSERVATIONS = pa.DataFrameSchema(
    {
        "dataset": pa.Column(str, pa.Check.isin(["international", "us_states"])),
        "unit_type": pa.Column(str, pa.Check.isin(["country", "us_state"])),
        "unit_id": pa.Column(str),
        "variable_id": pa.Column(str),
        "period": pa.Column(str),
        "value": pa.Column(float, nullable=True, coerce=True),
        "unit": pa.Column(str),
        "source_id": pa.Column(str),
        "file_path": pa.Column(str),
        "provenance": pa.Column(str, pa.Check.isin(["released", "reconstructed", "current"])),
    },
    unique=OBSERVATION_KEY,
    strict=True,
)


def validate_observations(frame: pd.DataFrame, registries: dict) -> pd.DataFrame:
    """Validate observation structure, finite values and unit registry membership."""
    frame = OBSERVATIONS.validate(frame)
    for dataset, expected_type in [("international", "country"), ("us_states", "us_state")]:
        selected = frame.loc[frame.dataset == dataset]
        if not selected.unit_type.eq(expected_type).all():
            raise ValueError(f"Unit type does not match {dataset}")
        unknown = set(selected.unit_id) - set(registries[dataset])
        if unknown:
            raise ValueError(f"Unknown units in {dataset}: {sorted(unknown)}")
    if np.isinf(frame.value.to_numpy()).any():
        raise ValueError("Infinite observation value")
    return frame


def validate_result_keys(frame: pd.DataFrame) -> None:
    """Reject duplicate identities, including duplicates across current variants."""
    keys = ["spec_id", "spec_version", "result_id", "variant_id"]
    if frame.duplicated(keys).any():
        raise ValueError("Duplicate result keys")
