#!/usr/bin/env python3
"""
Create golden_dataset.jsonl from a CSV manifest.
The script assumes:
    - Every row has an id, domain, source, path to raw excerpt,
      a pipe‑separated fact string, and a B1 summary string.
"""

import csv
import json
import pathlib
from typing import List

MANIFEST = pathlib.Path("manifest.csv")
OUTFILE = pathlib.Path("golden_dataset.jsonl")


def read_manifest(csv_path: pathlib.Path) -> List[dict]:
    rows = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            # Load the raw passage text
            excerpt_path = pathlib.Path(r["excerpt_path"])
            excerpt = excerpt_path.read_text(encoding="utf-8").strip()

            # Facts are stored in the CSV separated by "||"
            facts = [f.strip() for f in r["facts"].split("||") if f.strip()]
            assert len(facts) == 5, f"{r['id']} does not have exactly 5 facts."

            rows.append(
                {
                    "id": r["id"],
                    "domain": r["domain"],
                    "source": r["source"],
                    "excerpt": excerpt,
                    "facts": facts,
                    "summary_b1": r["summary_b1"].strip(),
                    # optional: add a notes column if you want
                    # "notes": r.get("notes", "").strip()
                }
            )
    return rows


def write_jsonl(records: List[dict], file_path: pathlib.Path) -> None:
    with file_path.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"✅ Wrote {len(records)} examples to {file_path}")


if __name__ == "__main__":
    data = read_manifest(MANIFEST)
    write_jsonl(data, OUTFILE)
