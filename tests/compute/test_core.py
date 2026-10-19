"""Independent hand-checkable examples of the numerical contract."""

import math

import numpy as np
import pandas as pd
import pytest

from lib.compute import correlation, index, standardise
from lib.transform import combine_sources, transform_values


def test_pearson_known_result_and_missing_pairs():
    # Centred cross-product is 4; both sums of squares are 5: r = 4/5.
    frame = pd.DataFrame(
        {"x": [1.0, 2.0, 3.0, 4.0, 99.0], "y": [1.0, 3.0, 2.0, 4.0, np.nan]}, index=list("ABCDE")
    )
    result = correlation(frame, "x", "y")
    assert result["r"] == pytest.approx(0.8)
    # For n=4, r=.8 gives t=4*sqrt(2)/3 and a two-sided p of .2.
    assert result["p"] == pytest.approx(0.2)
    assert result["n"] == 4
    assert list(result["observations"].index) == list("ABCD")
    shuffled = correlation(frame.sample(frac=1, random_state=3), "x", "y")
    assert shuffled["r"] == result["r"]
    pd.testing.assert_frame_equal(shuffled["observations"], result["observations"])


@pytest.mark.parametrize(
    "values,reason", [([1.0, 1.0, 1.0], "Constant"), ([1.0, np.nan, 2.0], "Fewer")]
)
def test_uncomputable_result_has_reason(values, reason):
    result = correlation(pd.DataFrame({"x": values, "y": [1.0, 2.0, 3.0]}), "x", "y")
    assert result["r"] is None and reason in result["reason"]


def test_transformations_preserve_missingness_and_direction():
    result = transform_values(pd.Series([1.0, math.e, np.nan]), "log", "reverse_coded")
    assert result.iloc[0] == 0
    assert result.iloc[1] == pytest.approx(-1)
    assert pd.isna(result.iloc[2])
    with pytest.raises(ValueError, match="positive"):
        transform_values(pd.Series([0.0]), "log", "as_is")


def test_zscore_reference_and_denominator():
    frame = pd.DataFrame({"a": [1.0, 2.0, 3.0, 100.0]}, index=list("ABCD"))
    result = standardise(frame, list("ABC"), 1)
    assert result.a.tolist() == [-1.0, 0.0, 1.0, 98.0]
    with pytest.raises(ValueError, match="Constant"):
        standardise(pd.DataFrame({"x": [1.0, 1.0]}), [0, 1], 1)


def test_index_available_components_and_weights():
    values = pd.DataFrame({"a": [1.0, 2.0, 3.0], "b": [1.0, np.nan, 3.0]}, index=list("ABC"))
    definition = {
        "components": ["a", "b"],
        "reference_units": list("ABC"),
        "ddof": 1,
        "weights": "equal",
        "missing_components": {"rule": "available_mean"},
    }
    result, report = index(values, definition)
    expected = -(1 + 1 / math.sqrt(2)) / 2
    assert result.loc["A"] == pytest.approx(expected)
    assert result.loc["B"] == 0.0
    assert result.loc["C"] == pytest.approx(-expected)
    assert len(report) == 6 and report.used.sum() == 5
    definition["missing_components"]["rule"] = "complete_cases"
    result, report = index(values, definition)
    assert pd.isna(result.loc["B"])
    assert not report.loc[report.unit_id.eq("B"), "used"].any()


@pytest.mark.parametrize("values", [[5.0, np.nan, np.nan], [np.nan, np.nan, np.nan]])
@pytest.mark.parametrize("rule", ["complete_cases", "available_mean"])
def test_index_rejects_components_without_a_standardisation_reference(values, rule):
    frame = pd.DataFrame({"a": [1.0, 2.0, 3.0], "b": values}, index=list("ABC"))
    definition = {
        "components": ["a", "b"],
        "reference_units": list("ABC"),
        "ddof": 1,
        "weights": "equal",
        "missing_components": {"rule": rule},
    }
    with pytest.raises(ValueError, match="Insufficient reference observations"):
        index(frame, definition)


def test_parallel_sources_never_average_and_reject_duplicate_keys():
    frame = pd.DataFrame(
        [
            ["international", "USA", "x", "2000", "primary", np.nan, "years"],
            ["international", "USA", "x", "2000", "secondary", 5.0, "years"],
        ],
        columns=["dataset", "unit_id", "variable_id", "period", "source_id", "value", "unit"],
    )
    assert combine_sources(frame, ["primary", "secondary"]).iloc[0].value == 5.0
    with pytest.raises(ValueError, match="Duplicate"):
        combine_sources(pd.concat([frame, frame]), ["primary", "secondary"])
    frame.loc[0, "unit"] = "days"
    with pytest.raises(ValueError, match="Conflicting units"):
        combine_sources(frame, ["primary", "secondary"])
