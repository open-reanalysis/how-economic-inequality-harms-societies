# SPDX-License-Identifier: MIT
# Purpose: Describe current index component availability before choosing an index rule.
# Thread: reproduction-lock
# Reads: historical component declarations, lineage and current presence flags
# Writes: outputs/tables/current_index_coverage.csv, docs/current-index-assessment.md and outputs/runs/
# Network: none

"""Assess candidate coverage without reading outcome magnitudes or computing associations."""

import csv

import yaml

from lib.paths import ROOT, sha256
from lib.runs import finish_run, start_run

if __name__ == "__main__":
    lineage_path = ROOT / "docs/source_lineage.csv"
    flags_path = ROOT / "outputs/tables/outcome_source_coverage.csv"
    lineage = list(csv.DictReader(lineage_path.open()))
    flags = list(csv.DictReader(flags_path.open()))
    rows, summaries, dependencies = [], [], [lineage_path, flags_path]
    for dataset in ["international", "us_states"]:
        spec_path = ROOT / f"config/specs/historical_{dataset}.yaml"
        dependencies.append(spec_path)
        spec = yaml.safe_load(spec_path.read_text())
        for component in spec["index"].get("components", []):
            matching = [
                r for r in lineage if r["dataset"] == dataset and r["variable_id"] == component
            ]
            record = matching[0] if matching else {}
            source = record.get("current_source", "")
            available = 0
            for unit in spec["samples"]["historical"]["units"]:
                found = (
                    [
                        f
                        for f in flags
                        if f["source_id"] == source
                        and f["unit_id"] == unit
                        and f["payload_status"] == "parsed"
                    ]
                    if source
                    else []
                )
                present = any(f["available"] == "True" for f in found) if found else None
                available += present is True
                rows.append(
                    {
                        "dataset": dataset,
                        "unit_id": unit,
                        "component": component,
                        "candidate_source": source,
                        "candidate_has_observation": present,
                        "candidate_periods": ";".join(
                            sorted({f["period"] for f in found if f["available"] == "True"})
                        ),
                        "comparability_class": record.get(
                            "comparability_class", "NOT_YET_VERIFIED"
                        ),
                        "assessment": record.get("deviation_reason", "See source lineage")
                        if found
                        else "No parsed current candidate available in this run; not evidence of absent series",
                    }
                )
            summaries.append(
                (dataset, component, available, len(spec["samples"]["historical"]["units"]))
            )
    output = ROOT / "outputs/tables/current_index_coverage.csv"
    with output.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    lines = [
        "# Current-index availability assessment",
        "",
        "This is a prospective availability assessment, not an index result or a reproduction lock. It uses only recorded presence flags across the acquisition window. A candidate observation in any year does not establish that an admissible observation exists for the final analysis period. Blank availability means no parsed candidate in this run, not an absent series.",
        "",
        "| Dataset | Historical component | Units with a nonmissing candidate in at least one acquired year | Master sample |",
        "|---|---|---:|---:|",
    ]
    lines += [f"| {d} | {c} | {n} | {total} |" for d, c, n, total in summaries]
    lines += [
        "",
        "## Consequences before locking",
        "",
        "The table separates source correspondence from availability. The lineage nominates conceptual successors for life expectancy, infant mortality, teenage births, homicide, imprisonment and education. WHO adult obesity is held as a substitute pending resolution of historical age/sex conventions; GDIM income elasticity is a substitute for the historical intergenerational income correlation. Neither substitute enters the primary series set merely because it downloaded successfully.",
        "",
        "The public WVS trust aggregate has been acquired, but weighting, denominator and country survey dates still require verification. Diagnostic mental-health prevalence still has an access/definition barrier. PISA 2025 mathematics/reading aggregates and Annex A2 population tables are held; sampling adjudication must accompany any selected observation. No acquired primary candidate covers all ten historical dimensions. The international primary index cannot currently reproduce the intended component set; its complete-case sample across all ten is empty. A substitute variant would still lack a verified trust measure and diagnostic mental-health prevalence, and mobility refers to cohorts rather than a recent annual period.",
        "",
        "Averaging only available dimensions changes the construct and gives countries different effective weights. Restricting to complete cases loses every country while unresolved components remain absent. A lower minimum, new weights or a wider date window would be scientific choices, not consequences of a download. No current index is calculated. On 19 October the maintainer rejected closing this work as not_produced and directed acquisition of missing components before locking. The lock therefore remains blocked on that acquisition and the resulting prospective method decisions.",
        "",
        "The U.S. state index has its own source targets. National international-series availability cannot fill state cells. The Census income request returned Missing Key HTML and current state outcome tables have not been parsed. State BRFSS mentally unhealthy days are distinct from diagnostic prevalence, corrected historical obesity differs from raw self-report, and national GSS trust cannot replace state identifiers.",
        "",
        "## Maintainer decision",
        "",
        "On 19 October 2026 the maintainer chose to defer the current-index lock until component availability and its consequences are documented. This assessment records the present evidence and exposes remaining verification work. It does not treat that decision as approval of a reduced index. Updated specifications and the executable lock remain in draft; no current association was computed.",
        "",
    ]
    document = ROOT / "docs/current-index-assessment.md"
    document.write_text("\n".join(lines))
    run = start_run("replay")
    run["steps"].append(
        {
            "target": "prospective-index-coverage",
            "state": "computed",
            "inputs": [
                {
                    "path": str(p.relative_to(ROOT)),
                    "sha256": sha256(p),
                    "check": "file_verified",
                    "restricted": False,
                }
                for p in dependencies
            ],
            "outputs": [
                {"path": str(p.relative_to(ROOT)), "sha256": sha256(p)} for p in [output, document]
            ],
        }
    )
    print(finish_run(run))
