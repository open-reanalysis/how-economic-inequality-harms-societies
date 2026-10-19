# SPDX-License-Identifier: MIT
# Purpose: Build the approved refreshed sample using no current outcome input.
# Thread: reproduction-lock
# Reads: config/eligibility.yaml and its declared income/population/membership inputs
# Writes: declared eligibility and survey tables, outputs/runs/
# Network: none

"""Produce the eligibility_table interface and survey evidence from pinned stored inputs."""

import json

import pandas as pd
import yaml

from lib.eligibility import eligibility, income_surveys, wdi_period
from lib.paths import ROOT, resolve, sha256
from lib.records import load_records, verify_files
from lib.runs import finish_run, start_run
from lib.schemas import ELIGIBILITY

if __name__ == "__main__":
    path = ROOT / "config/eligibility.yaml"
    rule = yaml.safe_load(path.read_text())
    if rule["status"] != "approved_rule":
        raise PermissionError("Eligibility rule has not been approved")
    _, acquisitions = load_records()
    verify_files(acquisitions)
    universe = pd.read_csv(resolve(rule["universe"]))
    records = json.loads(resolve(rule["inequality"]["path"]).read_text())
    surveys = income_surveys(records, rule["inequality"])
    frame = eligibility(
        universe,
        wdi_period(resolve(rule["ranking"]["path"]), rule["ranking"]["year"]),
        wdi_period(resolve(rule["population"]["path"]), rule["population"]["year"]),
        surveys,
        rule,
    )
    ELIGIBILITY.validate(frame)
    target, detail = resolve(rule["output"]), resolve(rule["detail_output"])
    target.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(target, index=False, na_rep="")
    surveys.to_csv(detail, index=False)
    inputs = [path, resolve(rule["universe"])]
    for name in ["ranking", "population", "inequality"]:
        inputs += [
            resolve(rule[name]["path"]),
            resolve(f"data/metadata/sources/{rule[name]['source_id']}.yaml"),
        ]
    run = start_run("replay")
    run["steps"].append(
        dict(
            target="refreshed-eligibility",
            state="computed",
            inputs=[
                dict(
                    path=str(p.relative_to(ROOT)),
                    sha256=sha256(p),
                    check="file_verified",
                    restricted=False,
                )
                for p in inputs
            ],
            outputs=[
                dict(path=str(p.relative_to(ROOT)), sha256=sha256(p)) for p in [target, detail]
            ],
        )
    )
    print(finish_run(run))
