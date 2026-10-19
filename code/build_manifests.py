# SPDX-License-Identifier: MIT
# Purpose: Generate flat source and acquisition views from canonical records.
# Thread: scaffold
# Reads: data/metadata/
# Writes: build/metadata/
# Network: none

"""Build disposable metadata views without introducing another maintained source."""

import pandas as pd

from lib.paths import ROOT
from lib.records import load_records

if __name__ == "__main__":
    sources, acquisitions = load_records()
    target = ROOT / "build/metadata"
    target.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(sources.values()).drop(columns=["reader_layout"], errors="ignore").to_csv(
        target / "sources.csv", index=False
    )
    pd.DataFrame([{k: v for k, v in a.items() if k != "files"} for a in acquisitions]).to_csv(
        target / "acquisitions.csv", index=False
    )
    pd.DataFrame([f for a in acquisitions for f in a["files"]]).to_csv(
        target / "files.csv", index=False
    )
    pd.DataFrame(
        [
            {"path": f["path"], "source_id": s}
            for a in acquisitions
            for f in a["files"]
            for s in f["source_ids"]
        ]
    ).to_csv(target / "file_sources.csv", index=False)
