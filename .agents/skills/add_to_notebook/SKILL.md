---
name: Add to Notebook
description: A meta-skill that bridges any researcher skill output into the paper notes website. Presents paper candidates for manual selection, then appends selected papers to papers.json, commits, and pushes to GitHub.
---

# Add to Notebook

## Purpose
After running any researcher skill (arXiv, Nature, bioRxiv, PNAS, etc.), this skill collects the paper candidates, asks the user which ones to add, builds the full `papers.json` schema for each, and automatically updates the website.

## When to Invoke
Invoke this skill **after** a researcher skill has presented its results, OR when the user says something like:
- "add these to the notebook"
- "add paper 1 and 3 to the website"
- "save this to the notebook"
- "update the website with these papers"

## Instructions for the Agent

### Step 1 — Present the Selection Menu
After the researcher skill returns results, display each paper as a numbered item with: title, journal, year, and a one-line summary. Example:

```
Found 5 papers. Which would you like to add to the notebook?

1. "Pan-genome of 26 maize lines..." | Nature Plants, 2024
   → Explores TE-driven regulatory variation using long-read assemblies
2. "Evo2: a foundation model for DNA..." | bioRxiv, 2024
   → DNA LM trained on 9.3T tokens, achieves SOTA on prokaryote/eukaryote tasks
...

Reply with numbers (e.g. "1, 3"), "all", or "none".
```

### Step 2 — Gather Full Schema for Each Selected Paper
For each selected paper, use `firecrawl_scrape` to fetch its abstract page and fill in ALL of the following fields:

| Field        | Description |
|---|---|
| `id`         | Unique slug: `{firstauthorlastname}{year}{firstkeyword}` e.g. `zhou2024maize` |
| `title`      | Full paper title |
| `authors`    | Array of author name strings (full names) |
| `journal`    | Exact journal name — must match one of the known journals: `Nature Plants`, `Nature Genetics`, `Nature Methods`, `Nature Biotechnology`, `Nature`, `Cell`, `Cell Genomics`, `Genome Biology`, `PNAS`, `bioRxiv`, `MBE`, `arXiv` |
| `year`       | Integer year of publication/preprint |
| `doi`        | DOI string only (without `https://doi.org/`) — if not available use `""` |
| `tags`       | Array of 3-6 short keyword strings |
| `rating`     | Evaluate the paper's relevance to the user's research interests from 1-5 and assign it an integer rating. 5 represents a critical, highly relevant paper. |
| `abstract`   | Full abstract text as a single string |
| `notes`      | AI-generated structured notes in the markdown template below |
| `addedDate`  | Today's date as `YYYY-MM-DD` |
| `source`     | Journal name (same as `journal`) |

**Notes template to fill in:**
```markdown
## Key Findings

- [bullet 1]
- [bullet 2]
- [bullet 3]

## Relevance to Our Work

[1-2 sentences on why this matters for plant genomics / DNA LMs / AI]

## Methods Worth Noting

- [method 1]
- [method 2]

## Questions / Follow-ups

- [ ] [question 1]
- [ ] [question 2]
```

### Step 3 — Append to papers.json
Run the Python helper script:

```bash
python3 .agents/skills/add_to_notebook/scripts/append_papers.py \
  --papers-json docs/js/papers.json \
  --new-entries 'new_papers_temp.json'
rm new_papers_temp.json
```

Where `new_papers_temp.json` is a temporary file you write in the current directory containing the array of new paper objects.

The script will:
- Load existing `papers.json`
- Skip any paper whose `id` already exists (deduplication)
- Append new valid entries
- Write back to `docs/js/papers.json`
- Print the result (how many added, how many skipped)

### Step 4 — Commit and Push
```bash
cd /Users/zhaijj/Documents/00PostDoc/Buckler_lab/GitHub/jingjing-paper-notebook
git add docs/js/papers.json
git commit -m "feat: add {n} paper(s) from {source} — {date}"
git push origin main
```

Where `{n}` is the count of added papers, `{source}` is the skill used (e.g. "Nature Journals"), and `{date}` is today's date.

### Step 5 — Confirm to User
Report back:
- How many papers were added vs. skipped (duplicates)
- The new total paper count
- A reminder that the live site at `https://zhaijj.github.io/jingjing-paper-notebook/` will update in ~1 minute

## Important Notes
- **Never overwrite** `papers.json` — always append.
- **Always deduplicate** by `id` before writing.
- If the DOI is not found, use `""` — do not guess.
- The `journal` field must exactly match the known journal names in the list above to get correct color coding on the website.
- If the paper is from a journal not in the known list, use the closest match or add it to both `papers.json` and tell the user the badge will default to gray.
