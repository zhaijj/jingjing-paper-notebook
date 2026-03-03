---
name: Daily ArXiv Researcher
description: A research assistant that uses Firecrawl to monitor the arXiv CS.AI section and summarize all relevant papers based on your interests.
---

# Daily ArXiv Researcher

## Purpose
This skill configures the agent to automatically scrape the recent submissions on arXiv's AI section and filter them based on your specific research directions (e.g., genomic language models, computational biology).

## Prerequisites
- The **Firecrawl MCP Server** must be running locally (`docker compose up -d`) and configured in the `mcp_config.json`.

## Instructions for the Agent

When the user invokes this skill, follow these exact steps:

1. **Scrape arXiv:** 
   Use the `firecrawl_scrape` tool to fetch the recent CS.AI listings from `https://arxiv.org/list/cs.AI/recent`. Request the output format as `markdown` and `onlyMainContent: true`.
2. **Filter & Select:** 
   Read the scraped markdown and identify all relevant papers based on the user's core research interests. Unless specified otherwise, assume the interests are: `genomic language model, computational biology, AI agent in biology`.
   - **RECENCY CONSTRAINT:** You MUST ONLY select papers from the most recent daily updates (i.e., submitted or updated within the last few days). Do not retrieve older papers.
3. **Fetch Abstracts:** 
   For each relevant paper, use the `firecrawl_scrape` tool again to fetch its dedicated abstract page (e.g., `https://arxiv.org/abs/xxxx.xxxxx`). This ensures you get the full abstract text and contribution details.
4. **Format Output:** 
   Present the final output using clear markdown headings and bullet points. For each paper, you MUST include:
   - The title and authors
   - A concise 2-3 sentence summary of the abstract
   - The core contribution/methodology
   - Direct markdown links to the abstract page and the PDF

## Example Output Format
```markdown
### 1. [Paper Title](https://arxiv.org/abs/xxxx.xxxxx)
*   **Authors:** Author 1, Author 2, etc.
*   **Abstract Summary:** [2-3 sentences summarising the abstract]
*   **Core Contribution:** [Brief description of the methodology]
*   **Links:** [Abstract Page](https://arxiv.org/abs/xxxx.xxxxx) | [PDF Direct Download](https://arxiv.org/pdf/xxxx.xxxxx)
```

## Step 5 — Offer to Add to Notebook
After presenting the results, always ask:

> "Would you like to add any of these to your paper notebook website? Reply with the numbers (e.g. **1, 3**), **all**, or **none**."

Then follow the **Add to Notebook** skill (`.agents/skills/add_to_notebook/SKILL.md`) to handle selection, schema building, and automatic commit + push to GitHub.
