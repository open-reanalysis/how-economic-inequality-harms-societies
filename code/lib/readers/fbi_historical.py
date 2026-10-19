"""FBI state-block reader; layout evidence is in the historical-reproduction log."""

import re

import pandas as pd


def read(path, source: dict, registry: dict) -> pd.DataFrame:
    """Read the declared rate row in each state block, preserving source suppression."""
    layout = source["reader_layout"]
    sheet = pd.read_excel(path, sheet_name=layout["sheet"], header=None).fillna("")
    if sheet.iloc[layout["header_row"], layout["value_column"]] != layout["expected_value_header"]:
        raise ValueError("FBI homicide column changed")
    aliases = {name.upper(): key for name, key in registry.items()}
    state = None
    rows = []
    for values in sheet.itertuples(index=False, name=None):
        label = str(values[0]).strip()
        cleaned = re.sub(r"\d+$", "", label)
        if cleaned in aliases:
            state = aliases[cleaned]
        elif cleaned in layout["excluded_labels"]:
            state = None
        elif label == layout["rate_label"] and state:
            value = values[layout["value_column"]]
            rows.append(
                {
                    "dataset": "us_states",
                    "unit_type": "us_state",
                    "unit_id": state,
                    "variable_id": layout["variable_id"],
                    "period": layout["period"],
                    "value": float(value) if value not in layout["missing_markers"] else None,
                    "unit": source["unit"],
                    "source_id": source["source_id"],
                    "file_path": source["input_path"],
                    "provenance": "reconstructed",
                }
            )
    frame = pd.DataFrame(rows)
    if frame.unit_id.duplicated().any():
        raise ValueError("Duplicate state rate in FBI table")
    return frame
