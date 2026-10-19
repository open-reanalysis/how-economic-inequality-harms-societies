"""Stored source-format examples independent of online services."""

import json

import pandas as pd
import pytest

from lib.readers.equality_trust import read as read_workbook
from lib.readers.worldbank import read as read_worldbank


def test_workbook_reader_maps_headers_and_preserves_missing(tmp_path):
    path = tmp_path / "example.xlsx"
    pd.DataFrame({"Country": ["Example A", "Example B"], "Published value": [2.0, None]}).to_excel(
        path, sheet_name="Data", index=False
    )
    source = {
        "source_id": "fixture",
        "input_path": "example.xlsx",
        "reader_layout": {
            "sheet": "Data",
            "unit_column": "Country",
            "dataset": "international",
            "unit_type": "country",
            "variables": [
                {"column": "Published value", "variable_id": "x", "period": "2000", "unit": "years"}
            ],
        },
    }
    frame = read_workbook(path, source, {"Example A": "AAA", "Example B": "BBB"})
    assert frame.unit_id.tolist() == ["AAA", "BBB"]
    assert frame.value.iloc[0] == 2 and pd.isna(frame.value.iloc[1])
    with pytest.raises(ValueError, match="Unknown workbook"):
        read_workbook(path, source, {})


def test_worldbank_reader_null_values_and_pagination(tmp_path):
    path = tmp_path / "response.json"
    payload = [{"pages": 1}, [{"countryiso3code": "USA", "date": "2025", "value": None}]]
    path.write_text(json.dumps(payload))
    source = {
        "source_id": "fixture",
        "input_path": "response.json",
        "variable_id": "x",
        "unit": "years",
    }
    frame = read_worldbank(path, source, {})
    assert frame.unit_id.tolist() == ["USA"] and pd.isna(frame.value.iloc[0])
    payload[0]["pages"] = 2
    path.write_text(json.dumps(payload))
    with pytest.raises(ValueError, match="paginated"):
        read_worldbank(path, source, {})
