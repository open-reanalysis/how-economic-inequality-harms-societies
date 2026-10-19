# SPDX-License-Identifier: MIT
# Purpose: Recover original country membership and presence flags from the stored release.
# Thread: original-access
# Reads: original release, source records and unit registry
# Writes: outputs/tables/original_sample_recovery.csv and outputs/runs/
# Network: none

"""Publish source-linked availability flags without copying the original observations."""

import csv

from lib.paths import ROOT, resolve, sha256
from lib.pipeline import registries
from lib.readers.equality_trust import read
from lib.records import load_records, verify_files
from lib.runs import finish_run, start_run

if __name__ == "__main__":
    sources, acquisitions = load_records()
    verify_files(acquisitions)
    source = sources["equalitytrust-international-release"]
    files = [f for a in acquisitions for f in a["files"] if source["source_id"] in f["source_ids"]]
    raw = resolve(files[0]["path"])
    if not raw.exists():
        print("Original local release absent; coverage cannot be recomputed.")
        raise SystemExit(0)
    _, aliases = registries()
    source = dict(source, input_path=files[0]["path"])
    frame = read(raw, source, aliases["international"])
    count = len(source["reader_layout"]["variables"])
    output = ROOT / "outputs/tables/original_sample_recovery.csv"
    run = start_run("replay")
    with output.open("w", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=[
                "dataset",
                "unit_id",
                "variable_id",
                "available",
                "source_id",
                "source_locator",
            ],
            lineterminator="\n",
        )
        writer.writeheader()
        for i, item in enumerate(frame.to_dict("records")):
            writer.writerow(
                {
                    "dataset": item["dataset"],
                    "unit_id": item["unit_id"],
                    "variable_id": item["variable_id"],
                    "available": bool(frame.value.notna().iloc[i]),
                    "source_id": item["source_id"],
                    "source_locator": f"{source['reader_layout']['sheet']}!R{i // count + 2}C{i % count + 2}",
                }
            )
    run["steps"].append(
        {
            "target": "original-sample-coverage",
            "state": "computed",
            "inputs": [
                {
                    "path": files[0]["path"],
                    "sha256": sha256(raw),
                    "check": "file_verified",
                    "restricted": True,
                }
            ],
            "outputs": [{"path": str(output.relative_to(ROOT)), "sha256": sha256(output)}],
        }
    )
    print(finish_run(run))
