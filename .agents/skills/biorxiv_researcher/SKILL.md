---
name: bioRxiv Researcher
description: A research assistant that uses Firecrawl to monitor the latest preprints on bioRxiv (specifically Bioinformatics, Genetics, Evolutionary Biology sections) and summarize papers based on your background in plant genomics, sequence modeling, and evolution.
---

# bioRxiv Researcher

## Purpose
This skill configures the agent to automatically scrape the recent submissions on bioRxiv and filter them based on your specific research expertise in DNA language models, plant genetics/evolution, and machine learning.

## Prerequisites
- The **Firecrawl MCP Server** must be running locally (`docker compose up -d`) and configured in the `mcp_config.json`.

## Target Sections
- Bioinformatics
- Genetics
- Evolutionary Biology
- Genomics

## Instructions for the Agent

When the user invokes this skill, follow these exact steps:

1. **Scrape bioRxiv:** 
   Use the `firecrawl_scrape` tool to fetch the latest research preprints from the target sections on bioRxiv (e.g., `https://www.biorxiv.org/collection/bioinformatics`, `https://www.biorxiv.org/collection/genetics`, etc.).
2. **Filter & Select:** 
   Read the scraped content and identify the 5 most relevant papers based on the user's core research background. The core research interests to prioritize are:
   - **DNA/Biological Language Models (Foundation Models):** applications to genomics, cross-species analysis, evolution, and population genetics/genomics.
   - **Plant Genomics and Evolution:** crop genomics, regulatory elements, whole-genome duplication.
   - **AI/Deep Learning Methods in Biology:** novel architectures applied to bioinformatics, RNA-seq, and sequence modeling.
3. **Fetch Abstracts:** 
   For each of the top 5 papers, use the `firecrawl_scrape` tool to fetch its dedicated abstract page on bioRxiv to get the full abstract text and preprint link.
4. **Format Output:** 
   Present the final output using clear markdown headings and bullet points. For each paper, you MUST include:
   - The Title and Authors
   - A concise 2-3 sentence summary of the abstract, highlighting the core biological/AI contribution
   - Why it is relevant to the user's specific research (e.g., "Relevant because it explores cross-species DNA foundation models").
   - Direct markdown links to the abstract page and PDF download.

## Example Output Format
```markdown
### 1. [Paper Title](https://www.biorxiv.org/content/xxxx)
*   **Authors:** Author 1, Author 2, etc.
*   **Abstract Summary:** [2-3 sentences summarising the abstract and main findings]
*   **Relevance:** [1 sentence explaining why it aligns with plant genomics, evolution, or biological AI]
*   **Links:** [Abstract Page](https://www.biorxiv.org/content/xxxx) | [PDF Direct Download](https://www.biorxiv.org/content/xxxx.full.pdf)
```

## Step 5 — Offer to Add to Notebook
After presenting the results, always ask:

> "Would you like to add any of these to your paper notebook website? Reply with the numbers (e.g. **1, 3**), **all**, or **none**."

Then follow the **Add to Notebook** skill (`.agents/skills/add_to_notebook/SKILL.md`) to handle selection, schema building, and automatic commit + push to GitHub.
