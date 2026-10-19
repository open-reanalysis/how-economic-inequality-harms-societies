"""Read the declared Census table layout; see historical-reproduction verification log."""

import pandas as pd


def read(path, source: dict, registry: dict) -> pd.DataFrame:
    """Extract state rates in the declared period; preserve suppressed observations as null."""
    layout = source["reader_layout"]
    frame = pd.read_excel(path, sheet_name=layout["sheet"], header=None)
    if str(int(frame.iat[layout["year_row"], layout["value_column"]])) != layout["period"]:
        raise ValueError("Census Statistical Abstract column year changed")
    rows = []
    for _, row in frame.iloc[layout["first_row"] : layout["last_row"] + 1].iterrows():
        name = str(row.iloc[layout["unit_column"]]).strip()
        if name in layout["excluded_labels"]:
            continue
        if name not in registry:
            raise ValueError(f"Unknown Census state label: {name}")
        raw = row.iloc[layout["value_column"]]
        value = (
            None if pd.isna(raw) or str(raw).strip() in layout["missing_markers"] else float(raw)
        )
        rows.append(
            dict(
                dataset="us_states",
                unit_type="us_state",
                unit_id=registry[name],
                variable_id=layout["variable_id"],
                period=layout["period"],
                value=value,
                unit=source["unit"],
                source_id=source["source_id"],
                file_path=source["input_path"],
                provenance="reconstructed",
            )
        )
    result = pd.DataFrame(rows)
    if result.unit_id.duplicated().any():
        raise ValueError("Duplicate state in Census Statistical Abstract table")
    return result
