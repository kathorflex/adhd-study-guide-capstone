#!/usr/bin/env python3
"""
Create golden_dataset.jsonl from manifest.csv
This is the authoritative golden dataset used for evaluation.
"""

import csv
import json
import pathlib
import sys


def create_golden_dataset():
    """Convert manifest CSV to golden dataset JSONL format."""

    project_root = pathlib.Path(__file__).parent.parent
    manifest_path = project_root / "data" / "manifest.csv"
    output_path = project_root / "data" / "golden_dataset.jsonl"

    if not manifest_path.exists():
        print(f"❌ Error: {manifest_path} not found!")
        print("   Run generate_raw_files.py first")
        sys.exit(1)

    print(f"📂 Reading manifest from: {manifest_path}")

    records = []

    with manifest_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            # Load the raw excerpt text
            excerpt_path = project_root / "data" / row["excerpt_path"]

            if not excerpt_path.exists():
                print(f"⚠️  Warning: {excerpt_path} not found, skipping {row['id']}")
                continue

            excerpt_text = excerpt_path.read_text(encoding="utf-8").strip()

            # Parse pipe-separated facts
            facts = [f.strip() for f in row["facts"].split("||") if f.strip()]

            if len(facts) != 5:
                print(f"⚠️  Warning: {row['id']} has {len(facts)} facts (expected 5)")

            record = {
                "id": row["id"],
                "domain": row["domain"],
                "source": row["source"],
                "excerpt": excerpt_text,
                "facts": facts,
                "summary_b1": row["summary_b1"].strip(),
            }

            records.append(record)
            print(f"✓ Processed: {row['id']} ({row['domain']})")

    # Write JSONL
    with output_path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"\n✅ Wrote {len(records)} examples to {output_path}")
    print(f"📊 Domains covered: {len(set(r['domain'] for r in records))}")


if __name__ == "__main__":
    create_golden_dataset()
