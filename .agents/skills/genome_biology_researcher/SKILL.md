---
name: Genome Biology Researcher
description: A research assistant that uses Firecrawl to monitor the latest publications in Genome Biology and summarize the most relevant papers based on your background in plant genomics, DNA language models, and AI.
---

# Genome Biology Researcher

## Purpose
This skill configures the agent to automatically scrape the recent publications from the journal Genome Biology and filter them based on your specific research expertise in plant genetics, DNA language models, and machine learning.

## Prerequisites
- The **Firecrawl MCP Server** must be running locally (`docker compose up -d`) and configured in the `mcp_config.json`.

## Target Journal
- Genome Biology (https://genomebiology.biomedcentral.com/)

## Instructions for the Agent

When the user invokes this skill, follow these exact steps:

1. **Scrape Journal Pages:** 
   Use the `firecrawl_scrape` tool (or `firecrawl_search`) to fetch the latest research articles, methods, and software from the Genome Biology journal.
2. **Filter & Select:** 
   Read the scraped content and identify the top 5 most relevant papers based on the user's core research background. The core research interests to prioritize are:
   - **DNA/Biological Language Models (Foundation Models):** applications to genomics, cross-species analysis, evolution, and population genetics/genomics.
   - **Plant Genomics and Evolution:** crop genomics, regulatory elements, whole-genome duplication.
   - **AI/Deep Learning Methods in Biology:** novel architectures applied to bioinformatics, RNA-seq, and sequence modeling.
3. **Fetch Abstracts:** 
   For each of the top 5 papers, use the `firecrawl_scrape` tool to fetch its dedicated abstract page on the Genome Biology website to get the full abstract text and DOI.
4. **Format Output:** 
   Present the final output using clear markdown headings and bullet points. For each paper, you MUST include:
   - The Journal Name, Title, and Authors
   - A concise 2-3 sentence summary of the abstract, highlighting the core biological/AI contribution
   - Why it is relevant to the user's specific research (e.g., "Relevant because it introduces a novel deep learning framework for plant genomics").
   - Direct markdown links to the abstract page.

## Example Output Format
```markdown
### 1. [Paper Title](https://genomebiology.biomedcentral.com/articles/XXXX) - *[Journal Name]*
*   **Authors:** Author 1, Author 2, etc.
*   **Abstract Summary:** [2-3 sentences summarising the abstract and main findings]
*   **Relevance:** [1 sentence explaining why it aligns with plant genomics or biological AI]
*   **Link:** [Abstract Page](https://genomebiology.biomedcentral.com/articles/XXXX)
```
