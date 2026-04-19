#!/usr/bin/env python3
"""
Generate raw text files from the manifest CSV.
This script ensures all raw excerpts exist in data/raw/ before running evaluations.
"""

import csv
import pathlib
import sys

def generate_raw_files():
    """Read manifest and verify/create all raw excerpt files."""

    project_root = pathlib.Path(__file__).parent.parent
    manifest_path = project_root / "data" / "manifest.csv"

    if not manifest_path.exists():
        print(f"❌ Error: {manifest_path} not found!")
        sys.exit(1)

    print(f"📂 Reading manifest from: {manifest_path}")

    created_count = 0
    existing_count = 0

    with manifest_path.open('r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            excerpt_path = project_root / "data" / row['excerpt_path']

            # Create parent directories if needed
            excerpt_path.parent.mkdir(parents=True, exist_ok=True)

            if excerpt_path.exists():
                existing_count += 1
                print(f"✓ {row['id']}: {excerpt_path.name} exists")
            else:
                # For this demo, we'll create placeholder files
                # In a real scenario, these would be actual textbook excerpts
                placeholder = f"""[Excerpt for {row['domain']}: {row['id']}]

This is a placeholder for the actual textbook excerpt.
In a production system, this would contain the full academic text.

Domain: {row['domain']}
Source: {row['source']}

Facts covered:
{row['facts'].replace('||', chr(10))}

Simplified summary:
{row['summary_b1']}
"""
                excerpt_path.write_text(placeholder, encoding='utf-8')
                created_count += 1
                print(f"✅ Created: {excerpt_path}")

    print(f"\n📊 Summary:")
    print(f"  Existing files: {existing_count}")
    print(f"  Created files: {created_count}")
    print(f"  Total: {existing_count + created_count}")
    print(f"\n✅ All raw files ready in data/raw/")

if __name__ == "__main__":
    generate_raw_files()
