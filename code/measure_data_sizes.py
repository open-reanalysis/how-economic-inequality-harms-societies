# SPDX-License-Identifier: MIT
# Purpose: Measure data file sizes to decide git, Git LFS or release asset per file.
# Thread: scaffold
# Reads: data/, sources/, the CANDIDATES list below
# Writes: outputs/logs/data_size_survey.csv
# Network: live sources (HTTP HEAD or a one-byte range request only, no data is downloaded)
"""Survey file sizes against GitHub's limits.

GitHub warns at 50 MiB and rejects files above 100 MiB in a normal git
object. Git LFS takes files up to 2 GiB on GitHub Free, so a file above 50 MiB
goes to LFS and only a file above that limit becomes a release asset.
"""

import csv
import datetime as dt
import pathlib
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "logs" / "data_size_survey.csv"
MIB = 1024 * 1024
WARN = 50 * MIB
LFS_MAX = 2 * 1024 * MIB

# Bulk files whose download URL is documented by the publisher. Sources served
# through query APIs (OECD SDMX, World Bank PIP, WHO GHO) have no fixed file size
# and are measured when the data threads acquire them.
CANDIDATES = [
    ("World Bank WDI bulk CSV", "https://databank.worldbank.org/data/download/WDI_CSV.zip"),
    ("WID.world all data bulk", "https://wid.world/bulk_download/wid_all_data.zip"),
    (
        "Spirit Level at 15 technical appendix",
        "https://eprints.whiterose.ac.uk/id/eprint/215026/7/Technical_Appendix_20_07.pdf",
    ),
]


def classify(size):
    """Return git, lfs or release_asset for a size in bytes, or unknown."""
    if size is None:
        return "unknown"
    if size <= WARN:
        return "git"
    if size <= LFS_MAX:
        return "lfs"
    return "release_asset"


def remote_size(url):
    """Return (size, note) from Content-Length or a one-byte Content-Range."""
    headers = {"User-Agent": "open-reanalysis-size-survey"}
    try:
        req = urllib.request.Request(url, method="HEAD", headers=headers)
        with urllib.request.urlopen(req, timeout=60) as r:
            length = r.headers.get("Content-Length")
            if length:
                return int(length), f"HEAD {r.status}"
        req = urllib.request.Request(url, headers={**headers, "Range": "bytes=0-0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            rng = r.headers.get("Content-Range", "")
            if "/" in rng and rng.split("/")[-1].isdigit():
                return int(rng.split("/")[-1]), f"range {r.status}"
            return None, f"no size header, status {r.status}"
    except (OSError, ValueError) as exc:  # the survey records failures instead of stopping
        return None, f"failed: {type(exc).__name__}: {exc}"[:200]


def main():
    now = dt.datetime.now(dt.UTC).isoformat(timespec="seconds")
    rows = []
    for folder in ("data", "sources"):
        for path in sorted((ROOT / folder).rglob("*")):
            if path.is_file() and path.name != ".gitkeep":
                size = path.stat().st_size
                rel = str(path.relative_to(ROOT))
                rows.append([now, "committed", rel, size, classify(size), ""])
    for name, url in CANDIDATES:
        size, note = remote_size(url)
        shown = size if size is not None else ""
        rows.append([now, "remote", f"{name} <{url}>", shown, classify(size), note])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["measured_utc", "kind", "path_or_source", "size_bytes", "storage", "note"])
        w.writerows(rows)
    for r in rows:
        print(r)


if __name__ == "__main__":
    main()
