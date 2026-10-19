"""Read the canonical observation interface, primarily for synthetic fixtures."""

import pandas as pd


def read(path, source: dict, registry: dict) -> pd.DataFrame:
    """Read CSV without losing leading zeros in state IDs or period identifiers."""
    return pd.read_csv(path, dtype={"unit_id": str, "period": str})
