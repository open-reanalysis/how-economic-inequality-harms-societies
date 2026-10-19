"""Read presence only from the official joint EVS/WVS frequency PDF.

Layout: docs/source_verification/index-counterparts.md, GESIS v5 report check.
"""

import re

from pypdf import PdfReader


def table_rows(text: str, count: int) -> dict[str, list[str]]:
    """Parse provider country/study rows, rejecting duplicate labels and malformed cells."""
    rows = {}
    pattern = r"^(.+?)\s+([\d,]+)\s+((?:\d+\.\d+|[-])(?:\s+(?:\d+\.\d+|[-]))*)$"
    for line in text.splitlines():
        match = re.fullmatch(pattern, line.strip())
        if not match:
            continue
        label, _, cells = match.groups()
        if label in rows:
            raise ValueError("Duplicate EVS/WVS country/study label")
        values = cells.split()
        if len(values) != count or any(v != "-" and not 0 <= float(v) <= 100 for v in values):
            raise ValueError("EVS/WVS table columns or percentage range changed")
        rows[label] = values
    return rows


def presence(year_text: str, trust_text: str, source: dict) -> list[dict]:
    """Return unit/survey-year/study presence without selecting a survey or exposing values."""
    layout = source["reader_layout"]
    if layout["year_header"] not in year_text or layout["question_header"] not in trust_text:
        raise ValueError("EVS/WVS year or trust question header changed")
    years = table_rows(year_text, len(layout["year_columns"]))
    trust = table_rows(trust_text, layout["response_columns"])
    result = []
    for label in sorted(source["unit_map"]):
        if label not in years or label not in trust:
            raise ValueError("Mapped EVS/WVS country/study missing from table")
        cells = years[label]
        positions = [i for i, value in enumerate(cells) if value == "100.0"]
        if len(positions) != 1 or any(v not in {"-", "100.0"} for v in cells):
            raise ValueError("EVS/WVS survey spans multiple reference years")
        study = label.rsplit(" ", 1)[-1] if label.endswith((" EVS", " WVS")) else "single"
        result.append(
            dict(
                unit_id=source["unit_map"][label],
                period=f"{layout['year_columns'][positions[0]]}_{study}",
                available=any(v != "-" for v in trust[label][:2]),
                quality_flag="gwght_all_response_denominator;survey_selection_pending",
            )
        )
    return result


def read_coverage(path, source: dict) -> list[dict]:
    """Read declared PDF pages; year denotes provider survey reference, not fieldwork bounds."""
    reader = PdfReader(path)
    layout = source["reader_layout"]
    texts = {
        key: "\n".join(reader.pages[i - 1].extract_text() for i in layout[key])
        for key in ["year_pages", "trust_pages"]
    }
    if layout["weight_marker"] not in texts["trust_pages"]:
        raise ValueError("EVS/WVS weighting marker changed")
    return presence(texts["year_pages"], texts["trust_pages"], source)
