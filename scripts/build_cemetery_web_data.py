#!/usr/bin/env python3
"""Package the cemetery CSV as browser data for local and hosted pages."""

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "cemetery_records" / "extracted" / "chinese_names.csv"
OUTPUT = ROOT / "cemetery-records-data.js"


with SOURCE.open(encoding="utf-8-sig", newline="") as source:
    records = list(csv.DictReader(source))

payload = json.dumps(records, ensure_ascii=False, separators=(",", ":"))
OUTPUT.write_text(
    "// Generated from cemetery_records/extracted/chinese_names.csv.\n"
    f"window.CEMETERY_RECORDS={payload};\n",
    encoding="utf-8",
)

print(f"Wrote {len(records)} records to {OUTPUT}")
