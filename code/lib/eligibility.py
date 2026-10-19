"""Eligibility uses income, population and survey metadata only, never outcome coverage."""

import json

import numpy as np
import pandas as pd


def wdi_period(path, year: int) -> dict:
    """Read one declared WDI period from a complete stored response, rejecting duplicate keys."""
    data = json.loads(path.read_text())
    if not isinstance(data, list) or len(data) != 2 or data[0]["pages"] != 1:
        raise ValueError("Incomplete WDI eligibility response")
    rows = [r for r in data[1] if r["date"] == str(year) and r["countryiso3code"]]
    keys = [r["countryiso3code"] for r in rows]
    if len(set(keys)) != len(keys):
        raise ValueError("Duplicate WDI country-period")
    return {r["countryiso3code"]: r["value"] for r in rows}


def income_surveys(records: list, rule: dict) -> pd.DataFrame:
    """Select latest observed national income distribution; output S80/S20 is dimensionless."""
    eligible = []
    for row in records:
        if any(
            row[k] != rule[k]
            for k in ["welfare_type", "reporting_level", "survey_coverage", "is_interpolated"]
        ):
            continue
        year = row["survey_year"]
        if not rule["earliest_year"] <= year <= rule["latest_year"]:
            continue
        if rule["reporting_equals_survey_year"] and row["reporting_year"] != year:
            continue
        shares = [row.get(f"decile{i}") for i in [1, 2, 9, 10]]
        if any(v is None or not np.isfinite(v) or v < 0 or v > 1 for v in shares):
            continue
        bottom, top = sum(shares[:2]), sum(shares[2:])
        if bottom <= 0 or top < bottom:
            continue
        eligible.append(
            dict(
                country=row["country_code"],
                survey_year=str(int(year)),
                survey_acronym=row["survey_acronym"],
                s80_s20=top / bottom,
            )
        )
    frame = pd.DataFrame(eligible, columns=["country", "survey_year", "survey_acronym", "s80_s20"])
    if frame.duplicated(["country", "survey_year"]).any():
        raise ValueError("Ambiguous income survey for one country-year")
    return frame.sort_values(["country", "survey_year"]).drop_duplicates("country", keep="last")


def eligibility(
    universe: pd.DataFrame, income: dict, population: dict, surveys: pd.DataFrame, rule: dict
) -> pd.DataFrame:
    """Rank the entire declared state universe before applying population and survey eligibility."""
    if universe.unit_id.duplicated().any():
        raise ValueError("Duplicate country in eligibility universe")
    frame = universe[["unit_id"]].rename(columns={"unit_id": "country"}).copy()
    frame["rank_value"] = pd.to_numeric(frame.country.map(income))
    if (frame.rank_value.dropna() <= 0).any():
        raise ValueError("Invalid ranking income")
    frame["rank"] = frame.rank_value.rank(method="min", ascending=False)
    frame["population"] = pd.to_numeric(frame.country.map(population)).astype(float)
    frame["comparable_inequality_data"] = frame.country.isin(surveys.country)
    reasons = []
    for row in frame.to_dict("records"):
        if pd.isna(row["rank"]):
            reason = "not_ranked"
        elif row["rank"] > rule["ranking"]["top_n"]:
            reason = "not_top_50"
        elif pd.isna(row["population"]):
            reason = "population_unavailable"
        elif row["population"] <= rule["population"]["minimum_exclusive"]:
            reason = "population_below_3m"
        elif not row["comparable_inequality_data"]:
            reason = "no_comparable_inequality_data"
        else:
            reason = ""
        reasons.append(reason)
    frame["eligible"] = [not r for r in reasons]
    frame["exclusion_reason"] = reasons
    return frame.sort_values("country")
