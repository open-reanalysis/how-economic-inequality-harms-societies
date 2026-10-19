"""Census historical state table reader; see historical-reproduction verification log."""

import csv

import pandas as pd


def read(path, source: dict, registry: dict) -> pd.DataFrame:
    """Extract the declared household-Gini column, excluding documented aggregate labels."""
    layout = source["reader_layout"]
    with path.open(newline="", encoding="utf-8-sig") as stream:
        rows = list(csv.reader(stream))
    header = next(i for i, row in enumerate(rows) if row and row[0] == layout["header_marker"])
    if rows[header][layout["value_column"]] != layout["period"]:
        raise ValueError("Census historical column year changed")
    result = []
    for row in rows[header + 1 :]:
        if not row or not row[0]:
            continue
        if row[0].startswith(layout["footer_prefix"]):
            break
        name = row[0].strip()
        if name in layout["excluded_labels"]:
            continue
        if name not in registry:
            raise ValueError(f"Unknown Census state label: {name}")
        result.append(
            {
                "dataset": "us_states",
                "unit_type": "us_state",
                "unit_id": registry[name],
                "variable_id": layout["variable_id"],
                "period": layout["period"],
                "value": float(row[layout["value_column"]]),
                "unit": source["unit"],
                "source_id": source["source_id"],
                "file_path": source["input_path"],
                "provenance": "reconstructed",
            }
        )
    frame = pd.DataFrame(result)
    if frame.unit_id.duplicated().any():
        raise ValueError("Duplicate state in Census historical table")
    return frame
