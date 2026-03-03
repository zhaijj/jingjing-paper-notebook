---
name: Cell Researcher
description: A research assistant that uses Firecrawl to monitor the latest publications in Cell and summarize the most relevant papers based on your background in plant genomics, DNA language models, and AI.
---

# Cell Researcher

## Purpose
This skill configures the agent to automatically scrape the recent publications from the journal Cell and filter them based on your specific research expertise in plant genetics, DNA language models, and machine learning.

## Prerequisites
- The **Firecrawl MCP Server** must be running locally (`docker compose up -d`) and configured in the `mcp_config.json`.

## Target Journal
- Cell (https://www.cell.com/cell/newarticles)

## Instructions for the Agent

When the user invokes this skill, follow these exact steps:

1. **Scrape Journal Pages:** 
   Use the `firecrawl_scrape` tool (or `firecrawl_search`) to fetch the latest research articles from the Cell journal website.
2. **Filter & Select:** 
   Read the scraped content and identify all relevant papers based on the user's core research background. The core research interests to prioritize are:
   - **DNA/Biological Language Models (Foundation Models):** applications to genomics, cross-species analysis, evolution, and population genetics/genomics.
   - **Plant Genomics and Evolution:** crop genomics, regulatory elements, whole-genome duplication.
   - **AI/Deep Learning Methods in Biology:** novel architectures applied to bioinformatics, RNA-seq, and sequence modeling.
   - **RECENCY CONSTRAINT:** You MUST ONLY select papers from the most recent publication issue. Do not retrieve or select older papers from past years or previous issues. If using `firecrawl_search`, specifically query for the "latest issue" or current month/year to avoid retrieving older highly-cited papers.
3. **Fetch Abstracts:** 
   For each relevant paper, use the `firecrawl_scrape` tool to fetch its dedicated abstract page on the Cell website to get the full abstract text and DOI.
4. **Format Output:** 
   Present the final output using clear markdown headings and bullet points. For each paper, you MUST include:
   - The Journal Name, Title, and Authors
   - A concise 2-3 sentence summary of the abstract, highlighting the core biological/AI contribution
   - Why it is relevant to the user's specific research (e.g., "Relevant because it explores evolutionary constraints using deep learning on genomic data").
   - Direct markdown links to the abstract page.

## Example Output Format
```markdown
### 1. [Paper Title](https://www.cell.com/cell/fulltext/XXXX) - *[Journal Name]*
*   **Authors:** Author 1, Author 2, etc.
*   **Abstract Summary:** [2-3 sentences summarising the abstract and main findings]
*   **Relevance:** [1 sentence explaining why it aligns with plant genomics or biological AI]
*   **Link:** [Abstract Page](https://www.cell.com/cell/fulltext/XXXX)
```

## Step 5 — Offer to Add to Notebook
After presenting the results, always ask:

> "Would you like to add any of these to your paper notebook website? Reply with the numbers (e.g. **1, 3**), **all**, or **none**."

Then follow the **Add to Notebook** skill (`.agents/skills/add_to_notebook/SKILL.md`) to handle selection, schema building, and automatic commit + push to GitHub.
