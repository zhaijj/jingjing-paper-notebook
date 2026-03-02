#!/usr/bin/env python3
"""
append_papers.py — Safely append new paper entries to papers.json.

Usage:
    python3 append_papers.py --papers-json docs/js/papers.json --new-entries /tmp/new_papers.json

The new-entries file should contain a JSON array of paper objects matching
the papers.json schema. Existing entries are deduplicated by 'id'.
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path


REQUIRED_FIELDS = {"id", "title", "authors", "journal", "year", "abstract"}

KNOWN_JOURNALS = {
    "Nature Plants", "Nature Genetics", "Nature Methods",
    "Nature Biotechnology", "Nature", "Cell", "Cell Genomics",
    "Genome Biology", "PNAS", "bioRxiv", "MBE", "arXiv",
}

TAG_ALIASES = {
    "maize": ["maize"],
    "foundation model": ["machine learning", "foundation model"],
    "llm agents": ["machine learning", "LLM agents"],
    "deep learning": ["machine learning", "deep learning"],
    "artificial intelligence": ["machine learning"],
    "ai agents": ["machine learning", "AI agents"],
    "ai design": ["machine learning", "AI design"]
}


def load_json(path: Path) -> list:
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"{path} must contain a JSON array at the top level.")
    return data


def validate_entry(entry: dict) -> list[str]:
    """Return a list of validation warnings (not hard errors)."""
    warnings = []
    for field in REQUIRED_FIELDS:
        if not entry.get(field):
            warnings.append(f"  ⚠  Missing required field: '{field}'")
    if entry.get("journal") and entry["journal"] not in KNOWN_JOURNALS:
        warnings.append(
            f"  ⚠  Unknown journal '{entry['journal']}' — badge will be gray. "
            f"Known: {', '.join(sorted(KNOWN_JOURNALS))}"
        )
    return warnings


def build_defaults(entry: dict) -> dict:
    """Fill in optional fields with sensible defaults."""
    today = date.today().isoformat()
    entry.setdefault("doi", "")
    
    raw_tags = entry.get("tags", [])
    normalized_tags = []
    for tag in raw_tags:
        lower_tag = tag.lower()
        if lower_tag in TAG_ALIASES:
            normalized_tags.extend(TAG_ALIASES[lower_tag])
        else:
            normalized_tags.append(tag)

    seen = set()
    deduped_tags = []
    for t in normalized_tags:
        if t.lower() not in seen:
            deduped_tags.append(t)
            seen.add(t.lower())
    entry["tags"] = deduped_tags

    entry.setdefault("rating", 3)
    entry.setdefault("notes", "")
    entry.setdefault("addedDate", today)
    entry.setdefault("source", entry.get("journal", ""))
    return entry


def main():
    parser = argparse.ArgumentParser(description="Append papers to papers.json")
    parser.add_argument(
        "--papers-json", required=True, type=Path,
        help="Path to the existing papers.json file"
    )
    parser.add_argument(
        "--new-entries", required=True, type=Path,
        help="Path to a JSON file containing an array of new paper objects"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show what would happen without writing anything"
    )
    args = parser.parse_args()

    # Load existing papers
    existing = load_json(args.papers_json)
    existing_ids = {p["id"] for p in existing if "id" in p}

    # Load new entries
    new_entries = load_json(args.new_entries)
    if not new_entries:
        print("No new entries provided. Nothing to do.")
        sys.exit(0)

    added = []
    skipped_dup = []
    skipped_invalid = []

    for entry in new_entries:
        paper_id = entry.get("id", "<no-id>")

        # Deduplication
        if paper_id in existing_ids:
            skipped_dup.append(paper_id)
            print(f"⏭  Skipped (duplicate id): {paper_id}")
            continue

        # Validation warnings
        warnings = validate_entry(entry)
        for w in warnings:
            print(w)

        # Fill defaults
        entry = build_defaults(entry)
        added.append(entry)
        existing_ids.add(paper_id)
        print(f"✅ Queued: {paper_id} — {entry.get('title', '')[:60]}")

    if not added:
        print(f"\nResult: 0 added, {len(skipped_dup)} duplicate(s), {len(skipped_invalid)} invalid.")
        sys.exit(0)

    if args.dry_run:
        print(f"\n[dry-run] Would add {len(added)} paper(s). Not writing.")
        sys.exit(0)

    # Write back
    updated = existing + added
    with open(args.papers_json, "w", encoding="utf-8") as f:
        json.dump(updated, f, indent=2, ensure_ascii=False)
        f.write("\n")  # trailing newline

    print(
        f"\n📚 Done: {len(added)} added, "
        f"{len(skipped_dup)} duplicate(s) skipped. "
        f"Total papers: {len(updated)}"
    )


if __name__ == "__main__":
    main()
