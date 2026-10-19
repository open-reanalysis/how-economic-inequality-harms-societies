"""Small numerical core, independent of source family and geography."""

import numpy as np
import pandas as pd
from scipy.stats import pearsonr


def standardise(values: pd.DataFrame, reference: list[str], ddof: int) -> pd.DataFrame:
    """Calculate z-scores using available reference units and the declared denominator."""
    reference_values = values.reindex(reference)
    deviation = reference_values.std(ddof=ddof)
    if deviation.dropna().eq(0).any():
        raise ValueError("Constant index component")
    return (values - reference_values.mean()) / deviation


def index(values: pd.DataFrame, definition: dict) -> tuple[pd.Series, pd.DataFrame]:
    """Average declared standardised components; apply only specified missingness rules."""
    components = definition["components"]
    if definition.get("status") == "UNRESOLVED":
        raise ValueError("Index method is unresolved")
    selected = values.reindex(columns=components)
    reference = definition["reference_units"]
    scores = standardise(selected, reference, definition["ddof"])
    weights = definition["weights"]
    if weights == "equal":
        weights = dict.fromkeys(components, 1.0)
    if set(weights) != set(components) or any(w <= 0 for w in weights.values()):
        raise ValueError("Index weights must be positive and cover the component set")
    weight_series = pd.Series(weights)
    denominator = scores.notna().mul(weight_series).sum(axis=1)
    result = scores.mul(weight_series).sum(axis=1, min_count=1) / denominator.replace(0, np.nan)
    rule = definition["missing_components"]["rule"]
    if rule == "complete_cases":
        result = result.where(selected.notna().all(axis=1))
    elif rule != "available_mean":
        raise ValueError(f"Unknown missing-component rule: {rule}")
    result = result.drop(index=[], errors="ignore").rename("index")
    result.loc[result.index.isin(definition.get("excluded_units", []))] = np.nan
    report = selected.notna().rename_axis(index="unit_id", columns="component").stack()
    report = report.rename("available").reset_index()
    report["used"] = report.available & report.unit_id.map(result.notna())
    return result, report


def correlation(values: pd.DataFrame, predictor: str, outcome: str) -> dict:
    """Compute pairwise Pearson r, two-sided p and n, or an explicit barrier."""
    missing_columns = {predictor, outcome} - set(values.columns)
    if missing_columns:
        return {
            "r": None,
            "p": None,
            "n": 0,
            "reason": "Missing variables: " + ", ".join(sorted(missing_columns)),
            "observations": pd.DataFrame(),
        }
    pairs = values[[predictor, outcome]].dropna().sort_index()
    n = len(pairs)
    reason = ""
    if n < 3:
        reason = "Fewer than three paired observations"
    elif (pairs.nunique() < 2).any():
        reason = "Constant comparison variable"
    if reason:
        return {"r": None, "p": None, "n": n, "reason": reason, "observations": pd.DataFrame()}
    if not np.isfinite(pairs.to_numpy()).all():
        raise ValueError("Nonfinite comparison observations")
    r, p = pearsonr(pairs[predictor], pairs[outcome])
    return {"r": float(r), "p": float(p), "n": n, "reason": "", "observations": pairs}
