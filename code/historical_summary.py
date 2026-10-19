# SPDX-License-Identifier: MIT
# Purpose: Summarise historical numerical agreements, discrepancies and barriers.
# Thread: historical-reproduction
# Reads: historical result tables, specifications and the result catalogue
# Writes: outputs/diagnostics/historical_reproduction_discrepancies.md and outputs/runs/
# Network: none

"""Report every comparison without treating a discrepancy as a software failure."""

import pandas as pd
import yaml

from lib.paths import ROOT, sha256
from lib.runs import finish_run, start_run

if __name__ == "__main__":
    catalogue_path = ROOT / "config/results_catalogue.csv"
    catalogue = pd.read_csv(catalogue_path, dtype=str).fillna("")
    lines = [
        "# Historical reproduction: differences and barriers",
        "",
        "The calculations below use the available release, not an independently verified copy of every publication's original analysis version. Numerical agreement is assessed at the source's declared precision; it does not establish identity of all original methods or observations.",
        "",
        "| Result | Published r | Recomputed r | n | Assessment |",
        "|---|---:|---:|---:|---|",
    ]
    inputs = [
        {
            "path": str(catalogue_path.relative_to(ROOT)),
            "sha256": sha256(catalogue_path),
            "check": "file_verified",
            "restricted": False,
        }
    ]
    run = start_run("replay")
    for path in sorted((ROOT / "outputs/tables").glob("historical_*_results.csv")):
        spec_path = ROOT / "config/specs" / (path.name.removesuffix("_results.csv") + ".yaml")
        spec = yaml.safe_load(spec_path.read_text())
        tolerance = spec.get("reported_value_check", {}).get("tolerance_r")
        inputs.extend(
            {
                "path": str(p.relative_to(ROOT)),
                "sha256": sha256(p),
                "check": "file_verified",
                "restricted": False,
            }
            for p in [path, spec_path]
        )
        for row in pd.read_csv(path).to_dict("records"):
            source = catalogue.loc[catalogue.result_id.eq(row["result_id"])].iloc[0]
            benchmark = source.reported_value
            if row["state"] == "not_produced":
                assessment = str(row["reason"])
                number = "—"
            else:
                number = f"{row['r']:.9f}"
                if not benchmark:
                    assessment = "No published numeric benchmark"
                elif tolerance is None:
                    assessment = "Computed; published-precision tolerance unresolved"
                elif abs(row["r"] - float(benchmark)) <= tolerance:
                    assessment = "Agrees at the declared published precision"
                else:
                    assessment = "Differs; cause unresolved; inspect source-version conflicts in the rationale"
            lines.append(
                f"| {row['result_id']} | {benchmark or '—'} | {number} | {row['n']} | {assessment} |"
            )
    lines += [
        "",
        "No input was changed to improve agreement. The supplied international index was used directly; independent rebuilding of its standardisation and missingness rules remains unverified. The state comparisons are listed as barriers, not as a completed numerical reconstruction. Current-data associations have not been computed.",
        "",
    ]
    output = ROOT / "outputs/diagnostics/historical_reproduction_discrepancies.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines))
    run["steps"].append(
        {
            "target": "historical-summary",
            "state": "computed",
            "inputs": inputs,
            "outputs": [{"path": str(output.relative_to(ROOT)), "sha256": sha256(output)}],
        }
    )
    print(finish_run(run))
