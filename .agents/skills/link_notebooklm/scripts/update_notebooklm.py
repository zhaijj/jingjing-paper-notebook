#!/usr/bin/env python3
"""
update_notebooklm.py — Link a NotebookLM notebook to an existing paper in papers.json.

Usage:
    python3 update_notebooklm.py \\
        --papers-json docs/js/papers.json \\
        --paper-id zhou2024maize \\
        --notebooklm-url "https://notebooklm.google.com/notebook/abc-xyz" \\
        --notebooklm-notes /tmp/nlm_notes.md
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Update a paper entry in papers.json with NotebookLM notes"
    )
    parser.add_argument(
        "--papers-json", required=True, type=Path,
        help="Path to papers.json"
    )
    parser.add_argument(
        "--paper-id", required=True,
        help="The paper ID to update (e.g. zhou2024maize)"
    )
    parser.add_argument(
        "--notebooklm-url", required=True,
        help="Full URL to the NotebookLM notebook"
    )
    parser.add_argument(
        "--notebooklm-notes", required=True, type=Path,
        help="Path to a markdown file containing the notes extracted from NotebookLM"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show what would happen without writing anything"
    )
    args = parser.parse_args()

    # Load papers.json
    if not args.papers_json.exists():
        print(f"❌ papers.json not found at: {args.papers_json}", file=sys.stderr)
        sys.exit(1)

    with open(args.papers_json, "r", encoding="utf-8") as f:
        papers = json.load(f)

    if not isinstance(papers, list):
        print("❌ papers.json must contain a JSON array.", file=sys.stderr)
        sys.exit(1)

    # Find the target paper
    target = next((p for p in papers if p.get("id") == args.paper_id), None)
    if target is None:
        print(f"❌ No paper found with id '{args.paper_id}'", file=sys.stderr)
        print(f"   Available IDs: {[p.get('id') for p in papers]}")
        sys.exit(1)

    # Load notes markdown
    if not args.notebooklm_notes.exists():
        print(f"❌ Notes file not found at: {args.notebooklm_notes}", file=sys.stderr)
        sys.exit(1)

    notes_text = args.notebooklm_notes.read_text(encoding="utf-8").strip()
    if not notes_text:
        print("❌ Notes file is empty.", file=sys.stderr)
        sys.exit(1)

    # Check if already linked
    already_has_url = target.get("notebooklm_url")
    already_has_notes = target.get("notebooklm_notes")

    if already_has_url or already_has_notes:
        print(f"⚠  Paper '{args.paper_id}' already has NotebookLM data.")
        print(f"   Existing URL: {already_has_url or '(none)'}")
        print(f"   Overwriting...")

    # Apply updates
    target["notebooklm_url"] = args.notebooklm_url
    target["notebooklm_notes"] = notes_text
    target["updatedDate"] = date.today().isoformat()   # bubble to top on sort

    if args.dry_run:
        print(f"\n[dry-run] Would update '{args.paper_id}' with:")
        print(f"  notebooklm_url: {args.notebooklm_url}")
        print(f"  notebooklm_notes: ({len(notes_text)} chars)\n")
        print(notes_text[:300] + ("..." if len(notes_text) > 300 else ""))
        sys.exit(0)

    # Write back
    with open(args.papers_json, "w", encoding="utf-8") as f:
        json.dump(papers, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"\n✅ Updated '{args.paper_id}' with NotebookLM notes.")
    print(f"   URL: {args.notebooklm_url}")
    print(f"   Notes preview: {notes_text[:120]}{'...' if len(notes_text) > 120 else ''}")


if __name__ == "__main__":
    main()
