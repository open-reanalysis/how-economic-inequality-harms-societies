"""Stored source-format examples independent of online services."""

import json

import pandas as pd
import pytest

from lib.readers.census_historical import read as read_census
from lib.readers.equality_trust import read as read_workbook
from lib.readers.fbi_historical import read as read_fbi
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


def test_census_reader_selects_household_column_and_excludes_aggregate(tmp_path):
    path = tmp_path / "s4.csv"
    path.write_text(
        "Title\nState,1999,1999\nUnited States,0.5,0.3\nAlabama,0.4,0.2\nDistrict of Columbia,0.6,0.4\nSOURCE: synthetic fixture\n"
    )
    source = {
        "source_id": "fixture",
        "input_path": "s4.csv",
        "unit": "gini_ratio",
        "reader_layout": {
            "header_marker": "State",
            "value_column": 1,
            "period": "1999",
            "variable_id": "inequality",
            "footer_prefix": "SOURCE:",
            "excluded_labels": ["United States", "District of Columbia"],
        },
    }
    frame = read_census(path, source, {"Alabama": "01"})
    assert frame.unit_id.tolist() == ["01"]
    assert frame.value.tolist() == [0.4]


def test_fbi_reader_footnote_header_and_missing_rate(tmp_path):
    path = tmp_path / "fbi.xlsx"
    pd.DataFrame(
        [
            ["Area", "Homicide"],
            ["ALABAMA4", ""],
            ["State Total", 20],
            ["Rate per 100,000 inhabitants", 2.0],
            ["ALASKA", ""],
            ["Rate per 100,000 inhabitants", ""],
            ["DISTRICT OF COLUMBIA5", ""],
            ["Rate per 100,000 inhabitants", 9.0],
        ]
    ).to_excel(path, sheet_name="Example", header=False, index=False)
    source = {
        "source_id": "fixture",
        "input_path": "fbi.xlsx",
        "unit": "per_100000",
        "reader_layout": {
            "sheet": "Example",
            "header_row": 0,
            "value_column": 1,
            "expected_value_header": "Homicide",
            "rate_label": "Rate per 100,000 inhabitants",
            "period": "1999",
            "variable_id": "homicides",
            "excluded_labels": ["DISTRICT OF COLUMBIA"],
            "missing_markers": ["", "-"],
        },
    }
    frame = read_fbi(path, source, {"Alabama": "01", "Alaska": "02"})
    assert frame.unit_id.tolist() == ["01", "02"]
    assert frame.value.iloc[0] == 2.0 and pd.isna(frame.value.iloc[1])


def test_statab_reader_declared_year_and_suppression(tmp_path):
    from lib.readers.census_statab import read

    path = tmp_path / "statab.xlsx"
    pd.DataFrame(
        [["year", 2002], ["Alabama", 4.0], ["Alaska", "(B)"], ["District of Columbia", 8.0]]
    ).to_excel(path, sheet_name="data", header=False, index=False)
    source = dict(
        source_id="fixture",
        input_path="statab.xlsx",
        unit="per_1000_live_births",
        reader_layout=dict(
            sheet="data",
            year_row=0,
            value_column=1,
            first_row=1,
            last_row=3,
            unit_column=0,
            period="2002",
            variable_id="infant_mortality",
            excluded_labels=["District of Columbia"],
            missing_markers=["(B)"],
        ),
    )
    frame = read(path, source, {"Alabama": "01", "Alaska": "02"})
    assert frame.unit_id.tolist() == ["01", "02"]
    assert frame.value.iloc[0] == 4.0 and pd.isna(frame.value.iloc[1])
    source["reader_layout"]["period"] = "2000"
    with pytest.raises(ValueError, match="year changed"):
        read(path, source, {"Alabama": "01", "Alaska": "02"})
