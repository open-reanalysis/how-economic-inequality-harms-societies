"""Specification-driven transformations without source-specific rules."""

import numpy as np
import pandas as pd


def transform_values(values: pd.Series, transformation: str, direction: str) -> pd.Series:
    """Apply the declared transform, then direction coding; missing values stay missing."""
    if transformation == "none":
        result = values.copy()
    elif transformation == "log":
        if (values.dropna() <= 0).any():
            raise ValueError("Log transform requires positive values")
        result = np.log(values)
    else:
        raise ValueError(f"Unsupported transformation: {transformation}")
    if direction == "reverse_coded":
        result = -result
    elif direction != "as_is":
        raise ValueError(f"Unsupported direction: {direction}")
    return result


def combine_sources(frame: pd.DataFrame, priorities: list[str]) -> pd.DataFrame:
    """Select the first nonmissing value in declared source order for each key."""
    keys = ["dataset", "unit_id", "variable_id", "period"]
    selected = frame[frame.source_id.isin(priorities)].copy()
    if selected.duplicated(keys + ["source_id"]).any():
        raise ValueError("Duplicate source observation")
    if selected.groupby(keys, dropna=False).unit.nunique().gt(1).any():
        raise ValueError("Conflicting units before source combination")
    selected["_priority"] = selected.source_id.map(dict(zip(priorities, range(len(priorities)))))
    return (
        selected.dropna(subset=["value"])
        .sort_values(keys + ["_priority"])
        .drop_duplicates(keys)
        .drop(columns="_priority")
        .reset_index(drop=True)
    )


def prepare(frame: pd.DataFrame, spec: dict, sample: list[str]) -> pd.DataFrame:
    """Select declared periods/sources/sample and pivot to one row per unit."""
    series = []
    for variable in spec["variables"]:
        if variable.get("status") == "UNRESOLVED":
            continue
        subset = frame[
            frame.variable_id.eq(variable["variable_id"])
            & frame.period.eq(str(variable["period"]))
            & frame.unit_id.isin(sample)
            & frame.dataset.eq(spec["dataset"])
        ]
        if subset.empty:
            continue
        if variable.get("conversion", "none") != "none":
            raise ValueError("A conversion must be implemented and tested before use")
        if not subset.unit.eq(variable["unit"]).all():
            raise ValueError(f"Unit mismatch for {variable['variable_id']}")
        combined = combine_sources(subset, variable["sources"])
        if combined.unit_id.duplicated().any():
            raise ValueError("More than one observation per unit after period selection")
        values = combined.set_index("unit_id").value
        values = transform_values(values, variable["transformation"], variable["direction"])
        series.append(values.rename(variable["variable_id"]))
    if not series:
        return pd.DataFrame(index=pd.Index(sorted(sample), name="unit_id"))
    return pd.concat(series, axis=1).reindex(sorted(sample)).rename_axis("unit_id")
