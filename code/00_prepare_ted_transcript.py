# SPDX-License-Identifier: MIT
# Purpose: Export the unedited English caption cues of the linked TED video as CSV.
# Thread: original-access
# Reads: sources/supporting/original-authors/wilkinson-2011-ted/captions.en.json3
# Writes: sources/supporting/original-authors/wilkinson-2011-ted/transcript.en.csv
# Network: none

"""Convert stored JSON3 captions to CSV without changing their text or timing."""

import argparse
import csv
import json
from pathlib import Path


def timestamp(milliseconds: int) -> str:
    """Return an integer millisecond offset as HH:MM:SS.mmm."""
    seconds, fraction = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}.{fraction:03}"


def main() -> None:
    """Write one CSV row per text-bearing caption event, in source order."""
    source_dir = (
        Path(__file__).resolve().parents[1]
        / "sources/supporting/original-authors/wilkinson-2011-ted"
    )
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=source_dir / "captions.en.json3")
    parser.add_argument("--output", type=Path, default=source_dir / "transcript.en.csv")
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(
            ["cue_id", "start_ms", "duration_ms", "end_ms", "start_time", "end_time", "text"]
        )
        cue_id = 0
        for event in data["events"]:
            if "segs" not in event:
                continue
            cue_id += 1
            start = event["tStartMs"]
            duration = event["dDurationMs"]
            end = start + duration
            text = "".join(segment.get("utf8", "") for segment in event["segs"])
            writer.writerow(
                [cue_id, start, duration, end, timestamp(start), timestamp(end), text]
            )


if __name__ == "__main__":
    main()
