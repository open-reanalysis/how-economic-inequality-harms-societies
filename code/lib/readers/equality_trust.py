"""Equality Trust workbook reader; layout evidence: original-access verification log."""

import pandas as pd


def read(path, source: dict, registry: dict) -> pd.DataFrame:
    """Map declared sheet/header fields to observations without transforming values."""
    layout = source["reader_layout"]
    frame = pd.read_excel(path, sheet_name=layout["sheet"], dtype={layout["unit_column"]: str})
    if frame[layout["unit_column"]].duplicated().any():
        raise ValueError("Duplicate workbook unit")
    expected = {layout["unit_column"]} | {v["column"] for v in layout["variables"]}
    if not expected.issubset(frame.columns):
        raise ValueError("Workbook layout changed")
    rows = []
    for item in frame.to_dict("records"):
        name = item[layout["unit_column"]]
        if name not in registry:
            raise ValueError(f"Unknown workbook country/state: {name}")
        for variable in layout["variables"]:
            rows.append(
                {
                    "dataset": layout["dataset"],
                    "unit_type": layout["unit_type"],
                    "unit_id": registry[name],
                    "variable_id": variable["variable_id"],
                    "period": str(variable["period"]),
                    "value": item[variable["column"]],
                    "unit": variable["unit"],
                    "source_id": source["source_id"],
                    "file_path": source["input_path"],
                    "provenance": "released",
                }
            )
    return pd.DataFrame(rows)
