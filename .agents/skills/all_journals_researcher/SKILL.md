---
name: All Journals Researcher
description: A master research assistant that runs ALL individual journal scrapers in parallel via subagents and presents a unified list of relevant new papers from every tracked source, letting the user select which to add to the notebook.
---

# All Journals Researcher

## Purpose
Run every tracked journal source simultaneously using **parallel browser subagents** and present a single, deduplicated, numbered list of relevant new papers. Each subagent handles a subset of sources independently, filters for relevance internally, and returns only a compact JSON list — keeping the main agent's context small.

## Covered Sources
| Group | Journal / Preprint Server |
|---|---|
| **A — Journals** | Nature, Nature Genetics, Nature Methods, Nature Biotechnology, Nature Plants, Science, Cell, Cell Genomics, Current Biology |
| **B — Genome Journals** | Genome Biology, Genome Research, MBE, PNAS |
| **C — Preprints** | bioRxiv (5 sections), arXiv (cs.AI, cs.LG, q-bio.GN, q-bio.QM) |

## Research Interests (applies across all sources)
- **DNA/Biological Language Models:** applications to genomics, cross-species analysis, evolution, population genetics.
- **Plant Genomics and Evolution:** crop genomics, regulatory elements, whole-genome duplication, pangenomes, T2T assemblies.
- **AI/Deep Learning in Biology:** novel architectures for bioinformatics, RNA-seq, sequence modeling, genome annotation.
- **RECENCY CONSTRAINT:** Only papers from the most recent issue/week. Do not retrieve older papers.

---

## Instructions for the Agent

### Step 1 — Launch Three Parallel Browser Subagents

Fire **all three subagents simultaneously** — do NOT wait for one to finish before starting the next.

Each subagent is given a focused task description (below). Set `RecordingName` to a short descriptive string. The subagent will return a JSON array of relevant papers.

---

#### Subagent A — High-Impact Journals (Nature family + Science + Cell family)

**Task for subagent A:**

```
You are a research filtering agent. Your job is to scrape journal TOC pages,
identify relevant papers, and return ONLY a compact JSON array.

RESEARCH INTERESTS (filter strictly to these):
- DNA/biological language models applied to genomics or sequences
- Plant genomics (crops, Arabidopsis, pangenomes, T2T assemblies, regulatory elements)
- AI/deep learning methods for genome annotation, variant effect prediction, sequence modeling
- Cross-species comparative genomics with computational methods
RECENCY: Only papers from the most recent issue/week.

STEP 1 — Scrape the following URLs IN PARALLEL using firecrawl_scrape with
formats=["json"] and jsonOptions to extract article lists. For each URL, use
this jsonOptions schema:
  prompt: "List all research article titles, author names, publication dates,
           and article URLs from this journal table of contents page."
  schema: {"articles": [{"title": "string", "authors": "string",
           "date": "string", "url": "string"}]}

URLs to scrape simultaneously:
- https://www.nature.com/nature/articles?type=article
- https://www.nature.com/ng/articles?type=article
- https://www.nature.com/nmeth/articles?type=article
- https://www.nature.com/nbt/articles?type=article
- https://www.nature.com/nplants/articles?type=article
- https://www.science.org/action/showFeed?type=etoc&feed=rss&jc=science
- https://www.cell.com/cell/newarticles
- https://www.cell.com/cell-genomics/newarticles
- https://www.cell.com/current-biology/newarticles

STEP 2 — For each URL that returns insufficient content (fewer than 3 articles),
fall back to firecrawl_search with:
  query: "site:[domain] 2026 plant genomics OR language model OR pangenome"
  limit: 10

STEP 3 — Filter all collected articles against the research interests above.
Keep only HIGH relevance papers. Be strict — only include papers that clearly
match at least one interest area.

STEP 4 — For each paper that passes filtering, fetch its abstract page using
firecrawl_scrape with formats=["json"] and jsonOptions:
  prompt: "Extract the paper title, all author names, abstract text, DOI,
           and publication date."
  schema: {"title": "string", "authors": "string", "abstract": "string",
           "doi": "string", "date": "string"}
Fetch all abstracts in parallel.

STEP 5 — Return ONLY a JSON array (no prose, no markdown). Each element:
{
  "title": "...",
  "authors": "First Author et al.",
  "journal": "Nature Genetics",  // exact journal name
  "date": "YYYY-MM-DD",
  "url": "https://...",
  "doi": "10.XXXX/...",
  "abstract": "Full abstract text...",
  "relevance": "One sentence: why this matches the research interests."
}

Return an empty array [] if no papers pass the filter.
```

---

#### Subagent B — Genome Journals (Genome Biology, Genome Research, MBE, PNAS)

**Task for subagent B:**

```
You are a research filtering agent. Your job is to scrape journal TOC pages,
identify relevant papers, and return ONLY a compact JSON array.

RESEARCH INTERESTS (filter strictly to these):
- DNA/biological language models applied to genomics or sequences
- Plant genomics (crops, Arabidopsis, pangenomes, T2T assemblies, regulatory elements)
- AI/deep learning methods for genome annotation, variant effect prediction, sequence modeling
- Cross-species comparative genomics with computational methods
RECENCY: Only papers from the most recent issue/week.

STEP 1 — Scrape the following URLs IN PARALLEL using firecrawl_scrape with
formats=["json"] and jsonOptions. For each URL, use this schema:
  prompt: "List all research article titles, author names, publication dates,
           and article URLs from this journal page."
  schema: {"articles": [{"title": "string", "authors": "string",
           "date": "string", "url": "string"}]}

URLs to scrape simultaneously:
- https://genomebiology.biomedcentral.com/
- https://genome.cshlp.org/content/current
- https://genome.cshlp.org/content/early/recent
- https://www.pnas.org/action/showFeed?type=etoc&feed=rss&jc=pnas

For MBE, use firecrawl_search directly (it frequently blocks scrapers):
  firecrawl_search(query="site:academic.oup.com/mbe 2026 plant genomics OR
                   language model OR pangenome OR genome evolution", limit=10)

STEP 2 — Filter all articles against the research interests. Keep only HIGH
relevance papers.

STEP 3 — For each paper that passes filtering, fetch its abstract page using
firecrawl_scrape with formats=["json"] and jsonOptions:
  prompt: "Extract the paper title, all author names, abstract text, DOI,
           and publication date."
  schema: {"title": "string", "authors": "string", "abstract": "string",
           "doi": "string", "date": "string"}
Fetch all abstracts in parallel.

STEP 4 — Return ONLY a JSON array (no prose, no markdown). Each element:
{
  "title": "...",
  "authors": "First Author et al.",
  "journal": "Genome Biology",  // exact journal name
  "date": "YYYY-MM-DD",
  "url": "https://...",
  "doi": "10.XXXX/...",
  "abstract": "Full abstract text...",
  "relevance": "One sentence: why this matches the research interests."
}

Return an empty array [] if no papers pass the filter.
```

---

#### Subagent C — Preprints (bioRxiv + arXiv)

**Task for subagent C:**

```
You are a research filtering agent. Your job is to scrape preprint RSS feeds,
identify relevant papers, and return ONLY a compact JSON array.

RESEARCH INTERESTS (filter strictly to these):
- DNA/biological language models applied to genomics or sequences
- Plant genomics (crops, Arabidopsis, pangenomes, T2T assemblies, regulatory elements)
- AI/deep learning methods for genome annotation, variant effect prediction, sequence modeling
- Cross-species comparative genomics with computational methods
RECENCY: Only papers posted in the last 7 days.

STEP 1 — Scrape ALL of the following RSS feed URLs IN PARALLEL using
firecrawl_scrape with formats=["markdown"] (RSS XML parses well as markdown).
Do NOT use proxy:"stealth" — these feeds are fully public.

bioRxiv RSS feeds:
- https://connect.biorxiv.org/biorxiv_xml.php?subject=bioinformatics
- https://connect.biorxiv.org/biorxiv_xml.php?subject=genetics
- https://connect.biorxiv.org/biorxiv_xml.php?subject=evolutionary-biology
- https://connect.biorxiv.org/biorxiv_xml.php?subject=genomics
- https://connect.biorxiv.org/biorxiv_xml.php?subject=plant-biology

arXiv RSS feeds (use the RSS endpoint, not the listing page):
- https://rss.arxiv.org/rss/cs.AI
- https://rss.arxiv.org/rss/cs.LG
- https://rss.arxiv.org/rss/q-bio.GN
- https://rss.arxiv.org/rss/q-bio.QM

NOTE for bioRxiv: The DOI is in <dc:identifier> as "doi:10.XXXX/..." —
strip the "doi:" prefix. The abstract is in <description>.
NOTE for arXiv: The arXiv ID is in the <link> field; DOI format is
"10.48550/arXiv.XXXX.XXXXX". Abstract is in <description>.

STEP 2 — Filter all entries against the research interests above. Be strict.
Each bioRxiv RSS entry already includes the abstract in <description>,
so you do NOT need to fetch individual abstract pages.

For arXiv, if the RSS description is too short (< 50 words), fetch the
abstract page: https://arxiv.org/abs/[id]

STEP 3 — Deduplicate within results (same paper may appear in multiple feeds).

STEP 4 — Return ONLY a JSON array (no prose, no markdown). Each element:
{
  "title": "...",
  "authors": "First Author et al.",
  "journal": "bioRxiv",  // or "arXiv"
  "date": "YYYY-MM-DD",
  "url": "https://...",
  "doi": "10.XXXX/...",
  "abstract": "Full abstract text...",
  "relevance": "One sentence: why this matches the research interests."
}

Return an empty array [] if no papers pass the filter.
```

---

### Step 2 — Collect and Deduplicate Results

Once all three subagents return their JSON arrays:

1. **Load `docs/js/papers.json`** and extract all existing `doi` and `title` values (case-insensitive).
2. **Merge** the three arrays into one list. Remove any paper whose DOI or title already exists in `papers.json`.
3. **Deduplicate within results** — the same paper may appear from both journal and preprint sources. Keep whichever entry has more complete data (prefer journal version over preprint if available).

---

### Step 3 — Present Unified Results

Group papers by source group. Present a **single, sequentially numbered list** across all sources.

```markdown
## New Relevant Papers — [Today's Date]

### Nature / Science / Cell Family
1. **[Title](URL)** | *Journal* | [Date]
   Authors: [First Author et al.]
   → [relevance sentence]

### Genome Journals
2. **[Title](URL)** | *Genome Biology* | [Date]
   ...

### bioRxiv Preprints
3. **[Title](URL)** | *bioRxiv* | [Date]
   ...

### arXiv Preprints
4. **[Title](URL)** | *arXiv* | [Date]
   ...
```

If a group has no relevant new papers, note: `*(No new relevant papers this week)*`

---

### Step 4 — Ask for Selection

After presenting all results, ask:

> "Would you like to add any of these to your paper notebook website? Reply with the numbers (e.g. **1, 3, 7**), **all**, or **none**."

Then follow the **Add to Notebook** skill (`.agents/skills/add_to_notebook/SKILL.md`) to handle building full `papers.json` entries, committing, and pushing to GitHub.

---

## Performance Notes
- **Context efficiency**: Each subagent filters internally and returns JSON only — the main agent context receives ~1–5 KB per subagent instead of 50–200 KB of raw markdown per source.
- **Speed**: All three subagents run in true parallel. Expect ~2–3 min total vs. 10+ min for the old serial approach.
- **Fallbacks**: If a subagent fails or returns an error, note the failure and proceed with the other two results rather than retrying.
- **bioRxiv DOI format**: `dc:identifier` contains `doi:10.XXXX/...` — strip the `doi:` prefix.
- **arXiv DOI format**: Use `10.48550/arXiv.XXXX.XXXXX` constructed from the arXiv ID.
