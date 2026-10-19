"""Exercise provider dimensions and missingness without any external requests."""

import json

import pandas as pd
import pytest

from lib.coverage import coverage


def test_who_sex_and_age_filters_and_pagination(tmp_path):
    source = dict(
        coverage_format="who_odata", coverage_filters={"Dim1": "SEX_BTSX", "Dim2": "ADULT"}
    )
    row = dict(SpatialDim="AAA", TimeDim=2024, Dim1="SEX_BTSX", Dim2="ADULT", NumericValue=1)
    path = tmp_path / "who.json"
    payload = dict(value=[row, dict(row, Dim1="SEX_MLE"), dict(row, Dim2="CHILD")])
    path.write_text(json.dumps(payload))
    assert coverage(source, path) == [dict(unit_id="AAA", period="2024", available=True)]
    payload["@odata.nextLink"] = "https://example.invalid/page2"
    path.write_text(json.dumps(payload))
    with pytest.raises(ValueError, match="Incomplete"):
        coverage(source, path)


def test_prison_filter_suppression_and_duplicate_jurisdiction(tmp_path):
    source = dict(
        coverage_format="excel_rows",
        reader_layout=dict(
            sheet="data",
            header_row=0,
            filters={"indicator": "stock"},
            minimum_year=2020,
            country_column="country",
            year_column="year",
            value_column="value",
        ),
    )
    rows = [
        dict(country="AAA", year=2024, value=10, indicator="stock"),
        dict(country="BBB", year=2024, value="..", indicator="stock"),
        dict(country="AAA", year=2024, value=100, indicator="admissions"),
    ]
    path = tmp_path / "prison.xlsx"
    pd.DataFrame(rows).to_excel(path, sheet_name="data", index=False)
    assert coverage(source, path) == [
        dict(unit_id="AAA", period="2024", available=True),
        dict(unit_id="BBB", period="2024", available=False),
    ]
    pd.DataFrame(rows + [rows[0]]).to_excel(path, sheet_name="data", index=False)
    with pytest.raises(ValueError, match="Duplicate"):
        coverage(source, path)


def test_mobility_cohort_is_not_publication_year(tmp_path):
    path = tmp_path / "mobility.dta"
    pd.DataFrame(dict(code=["AAA", "BBB"], IGE=[0.1, float("nan")])).to_stata(
        path, write_index=False
    )
    rows = coverage(
        dict(
            coverage_format="stata",
            country_column="code",
            value_column="IGE",
            period_label="cohorts_1980s_1990s",
        ),
        path,
    )
    assert rows == [
        dict(unit_id="AAA", period="cohorts_1980s_1990s", available=True),
        dict(unit_id="BBB", period="cohorts_1980s_1990s", available=False),
    ]
