"""Replay accepts floating-point noise, never sample or result-identity changes."""

import pandas as pd
import pytest

from check_replay import compare


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
