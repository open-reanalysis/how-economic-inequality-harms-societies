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


def test_pisa_requires_both_domains_and_preserves_sampling_marker(tmp_path):
    path = tmp_path / "pisa.xlsx"
    with pd.ExcelWriter(path) as writer:
        pd.DataFrame([["Country", "Mean"], ["A*", 400], ["B", "m"]]).to_excel(
            writer, sheet_name="reading", header=False, index=False
        )
        pd.DataFrame([["Country", "Mean"], ["A*", 500], ["B", 400]]).to_excel(
            writer, sheet_name="math", header=False, index=False
        )
    source = dict(
        coverage_format="pisa_summary",
        reference_period="2025",
        unit_map={"A": "AAA", "B": "BBB"},
        reader_layout=dict(
            sheets=["reading", "math"],
            header_row=0,
            value_column=1,
            unit_column=0,
            expected_header="Mean",
            first_row=1,
            last_row=2,
        ),
    )
    assert coverage(source, path) == [
        dict(unit_id="AAA", period="2025", available=True, quality_flag="provider_asterisk"),
        dict(unit_id="BBB", period="2025", available=False, quality_flag="no_asterisk"),
    ]


def test_wvs_pooled_total_is_not_a_country_and_britain_is_not_uk(tmp_path):
    path = tmp_path / "trust.html"
    path.write_text(
        """<table><tr><td>TOTAL</td><td>ISO 3166-1 numeric country code</td></tr><tr><td>A</td><td>Great Britain</td></tr><tr><td>Most people can be trusted</td><td>20%</td><td>10%</td><td>30%</td></tr></table>"""
    )
    source = dict(
        coverage_format="wvs_country_html", reference_period="wave7", unit_map={"A": "AAA"}
    )
    assert coverage(source, path) == [
        dict(
            unit_id="AAA",
            period="wave7",
            available=True,
            quality_flag="weight_and_survey_year_unverified",
        )
    ]
    path.write_text(path.read_text().replace("Most people can be trusted", "Trust the police"))
    with pytest.raises(ValueError, match="question changed"):
        coverage(source, path)


def test_joint_wvs_keeps_studies_and_rejects_ambiguous_years():
    from lib.readers.wvs_joint import presence

    source = dict(
        unit_map={"A EVS": "AAA", "A WVS": "AAA", "B": "BBB"},
        reader_layout=dict(
            year_columns=[2018, 2022],
            year_header="2018 2022",
            question_header="A165- Most people can be trusted",
            response_columns=5,
        ),
    )
    years = "2018 2022\nA EVS 100 100.0 -\nA WVS 150 - 100.0\nB 20 100.0 -"
    trust = "A165- Most people can be trusted\nA EVS 100 20.0 70.0 5.0 5.0 -\nA WVS 150 30.0 70.0 - - -\nB 20 - 100.0 - - -\nGreat Britain 10 40.0 60.0 - - -"
    rows = presence(years, trust, source)
    assert [(r["unit_id"], r["period"], r["available"]) for r in rows] == [
        ("AAA", "2018_EVS", True),
        ("AAA", "2022_WVS", True),
        ("BBB", "2018_single", True),
    ]
    assert all("value" not in row for row in rows)
    with pytest.raises(ValueError, match="multiple reference years"):
        presence(years.replace("150 - 100.0", "150 50.0 50.0"), trust, source)
    with pytest.raises(ValueError, match="Duplicate"):
        presence(years + "\nB 20 100.0 -", trust, source)
    with pytest.raises(ValueError, match="header changed"):
        presence(years, trust.replace("A165-", "A166-"), source)
    with pytest.raises(ValueError, match="missing from table"):
        presence(years, trust.replace("B 20 - 100.0 - - -", ""), source)
    with pytest.raises(ValueError, match="percentage range"):
        presence(years, trust.replace("20.0 70.0", "120.0 70.0"), source)
