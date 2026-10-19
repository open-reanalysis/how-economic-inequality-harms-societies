"""Read World Bank v2 JSON responses, preserving provider units and periods."""

import json

import pandas as pd


def read(path, source: dict, registry: dict) -> pd.DataFrame:
    """Read one complete indicator response; fail on pagination or API error payloads."""
    data = json.loads(path.read_text())
    if not isinstance(data, list) or len(data) != 2 or not isinstance(data[1], list):
        raise ValueError("World Bank API did not return an indicator response")
    if data[0]["pages"] != 1:
        raise ValueError("World Bank response is paginated; acquire all pages separately")
    rows = []
    for item in data[1]:
        unit_id = item["countryiso3code"]
        if not unit_id:
            continue
        rows.append(
            {
                "dataset": "international",
                "unit_type": "country",
                "unit_id": unit_id,
                "variable_id": source["variable_id"],
                "period": str(item["date"]),
                "value": item["value"],
                "unit": source["unit"],
                "source_id": source["source_id"],
                "file_path": source["input_path"],
                "provenance": "current",
            }
        )
    return pd.DataFrame(rows)
