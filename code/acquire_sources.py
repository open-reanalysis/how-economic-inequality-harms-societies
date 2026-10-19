# SPDX-License-Identifier: MIT
# Purpose: Acquire explicitly declared source requests without calculating associations.
# Thread: scaffold
# Reads: config/acquisition_requests.yaml and data/metadata/sources/
# Writes: recorded raw files, acquisition records, retrieval logs and outputs/runs/
# Network: live sources

"""Download only requests declared before acquisition, with immutable paths."""

import argparse

import yaml

from lib.download import acquire
from lib.paths import ROOT, resolve, sha256
from lib.records import load_records
from lib.runs import finish_run, start_run

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", help="Acquire only this source ID")
    args = parser.parse_args()
    sources, existing = load_records()
    declared = yaml.safe_load((ROOT / "config/acquisition_requests.yaml").read_text())
    run = start_run("acquire")
    for request in declared["requests"]:
        source_id = request["source_id"]
        if args.source and args.source != source_id:
            continue
        if resolve(request["path"]).exists():
            run["skipped_steps"].append(source_id + ": immutable response already present")
            continue
        if source_id not in sources:
            raise ValueError(f"Unknown request source: {source_id}")
        record = acquire(
            [source_id],
            request["url"],
            request["path"],
            redistributable=sources[source_id]["redistributable"],
            post_form=request.get("post_form"),
        )
        paths = [file["path"] for file in record["files"]]
        paths += [
            record["retrieval_log"],
            f"data/metadata/acquisitions/{record['acquisition_id']}.yaml",
        ]
        run["steps"].append(
            {
                "target": source_id,
                "state": "computed" if record["status"] == "acquired" else "not_produced",
                "reason": record["notes"],
                "inputs": [],
                "outputs": [{"path": path, "sha256": sha256(resolve(path))} for path in paths],
            }
        )
        print(source_id, record["status"], record["response_status"], flush=True)
    print(finish_run(run))
