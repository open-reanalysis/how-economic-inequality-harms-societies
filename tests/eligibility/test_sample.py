"""Check prospective sample rules with synthetic data, never current outcomes."""

import pandas as pd
import pytest

from lib.eligibility import eligibility, income_surveys


@pytest.fixture
def rule():
    return dict(
        ranking=dict(top_n=2),
        population=dict(minimum_exclusive=3_000_000),
        inequality=dict(
            earliest_year=2020,
            latest_year=2025,
            welfare_type="income",
            reporting_level="national",
            survey_coverage="national",
            is_interpolated=False,
            reporting_equals_survey_year=True,
        ),
    )


def test_rank_before_population_filter_and_include_cutoff_ties(rule):
    units = pd.DataFrame(dict(unit_id=["AAA", "BBB", "CCC", "DDD"]))
    surveys = pd.DataFrame(dict(country=["AAA", "BBB", "CCC", "DDD"]))
    frame = eligibility(
        units,
        dict(AAA=100, BBB=90, CCC=90, DDD=80),
        dict(AAA=3_000_000, BBB=4_000_000, CCC=4_000_000, DDD=4_000_000),
        surveys,
        rule,
    ).set_index("country")
    assert frame.loc["AAA", "exclusion_reason"] == "population_below_3m"
    assert set(frame.index[frame.eligible]) == {"BBB", "CCC"}
    assert frame.loc["DDD", "exclusion_reason"] == "not_top_50"
    reversed_frame = eligibility(
        units.iloc[::-1],
        dict(AAA=100, BBB=90, CCC=90, DDD=80),
        dict(AAA=3_000_000, BBB=4_000_000, CCC=4_000_000, DDD=4_000_000),
        surveys,
        rule,
    )
    pd.testing.assert_frame_equal(
        frame.reset_index().reset_index(drop=True), reversed_frame.reset_index(drop=True)
    )


def test_observed_income_only_and_latest_matching_survey(rule):
    row = dict(
        country_code="AAA",
        welfare_type="income",
        reporting_level="national",
        survey_coverage="national",
        is_interpolated=False,
        survey_year=2020,
        reporting_year=2020,
        survey_acronym="fixture",
        decile1=0.02,
        decile2=0.03,
        decile9=0.2,
        decile10=0.3,
    )
    rows = [
        row,
        dict(row, survey_year=2022, reporting_year=2022),
        dict(row, country_code="BBB", welfare_type="consumption"),
        dict(row, country_code="CCC", is_interpolated=True),
        dict(row, country_code="DDD", survey_year=2019),
        dict(row, country_code="EEE", reporting_level="urban"),
        dict(row, country_code="FFF", decile1=0, decile2=0),
        dict(row, country_code="GGG", decile10=None),
    ]
    selected = income_surveys(rows, rule["inequality"])
    assert selected.country.tolist() == ["AAA"]
    assert selected.survey_year.tolist() == ["2022"]
    assert selected.s80_s20.tolist() == [10]
    with pytest.raises(ValueError, match="Ambiguous"):
        income_surveys([row, row], rule["inequality"])


def test_missing_population_is_not_below_threshold(rule):
    frame = eligibility(
        pd.DataFrame(dict(unit_id=["AAA", "BBB"])),
        dict(AAA=100),
        {},
        pd.DataFrame(dict(country=[])),
        rule,
    )
    assert frame.exclusion_reason.tolist() == ["population_unavailable", "not_ranked"]
