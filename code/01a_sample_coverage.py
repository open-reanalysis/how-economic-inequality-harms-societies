# SPDX-License-Identifier: MIT
# Purpose: Recover original country membership and presence flags from the stored release.
# Thread: original-access
# Reads: original release, source records and unit registry
# Writes: outputs/tables/original_sample_recovery.csv and outputs/runs/
# Network: none

"""Publish source-linked availability flags without copying the original observations."""

import csv
import json

from lib.paths import ROOT, resolve, sha256
from lib.pipeline import registries
from lib.readers.equality_trust import read
from lib.records import load_records, verify_files
from lib.runs import code_digest, finish_run, start_run

if __name__ == "__main__":
    sources, acquisitions = load_records()
    verify_files(acquisitions)
    source = sources["equalitytrust-international-release"]
    files = [f for a in acquisitions for f in a["files"] if source["source_id"] in f["source_ids"]]
    raw = resolve(files[0]["path"])
    output = ROOT / "outputs/tables/original_sample_recovery.csv"
    source_path = ROOT / "data/metadata/sources/equalitytrust-international-release.yaml"
    registry_path = ROOT / "config/units/countries.csv"
    expected = {
        files[0]["path"]: files[0]["sha256"],
        str(source_path.relative_to(ROOT)): sha256(source_path),
        str(registry_path.relative_to(ROOT)): sha256(registry_path),
    }
    if not raw.exists():
        run = start_run("replay")
        run["missing_inputs"] = [files[0]["path"]]
        producer = None
        for path in sorted((ROOT / "outputs/runs").glob("*.json"), reverse=True):
            earlier = json.loads(path.read_text())
            if earlier.get("code_sha256") != code_digest():
                continue
            for step in earlier["steps"]:
                if step["target"] != "original-sample-coverage" or step["state"] != "computed":
                    continue
                if (
                    {i["path"]: i["sha256"] for i in step["inputs"]} == expected
                    and output.exists()
                    and step["outputs"][0]["sha256"] == sha256(output)
                ):
                    producer = earlier["run_id"]
                    break
            if producer:
                break
        if not producer:
            raise SystemExit(
                "No compatible producer for restricted original coverage; recompute locally before publishing a new snapshot"
            )
        run["steps"].append(
            {
                "target": "original-sample-coverage",
                "state": "retained",
                "producer_run": producer,
                "reason": "Restricted release absent; code, metadata and recorded raw identity match",
                "inputs": [
                    {
                        "path": p,
                        "sha256": h,
                        "check": "record_matched" if p == files[0]["path"] else "file_verified",
                        "restricted": p == files[0]["path"],
                    }
                    for p, h in expected.items()
                ],
                "outputs": [{"path": str(output.relative_to(ROOT)), "sha256": sha256(output)}],
            }
        )
        print(finish_run(run))
        raise SystemExit(0)
    _, aliases = registries()
    source = dict(source, input_path=files[0]["path"])
    frame = read(raw, source, aliases["international"])
    count = len(source["reader_layout"]["variables"])
    output = ROOT / "outputs/tables/original_sample_recovery.csv"
    run = start_run("replay")
    run["code_sha256"] = code_digest()
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
                    "path": p,
                    "sha256": h,
                    "check": "file_verified",
                    "restricted": p == files[0]["path"],
                }
                for p, h in expected.items()
            ],
            "outputs": [{"path": str(output.relative_to(ROOT)), "sha256": sha256(output)}],
        }
    )
    print(finish_run(run))
