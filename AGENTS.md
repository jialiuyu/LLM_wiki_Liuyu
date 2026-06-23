# AGENTS.md - LLM Wiki Schema

This file is the operating schema for agents maintaining this repository.
Follow it before editing wiki content.

## Mission

Maintain a persistent, source-backed Markdown wiki. The user curates sources,
sets priorities, and reviews outputs. The agent does the maintenance work:
summarizing, filing, linking, revising, detecting contradictions, and keeping
the index and log current.

## Non-Negotiable Invariants

- `raw/` is the source-of-truth layer. Do not edit source contents. Do not move
  files out of `raw/inbox/` unless the user explicitly asks.
- `wiki/` is agent-maintained. It may be edited freely when following the
  workflows below.
- `AGENTS.md` is the schema. Propose schema changes when the wiki's needs
  change, then edit this file only when the user accepts or asks you to.
- `wiki/index.md` must be updated whenever pages are created, renamed, or
  materially changed.
- `wiki/log.md` is append-only. Add entries; do not rewrite history except to
  fix obvious formatting mistakes in the entry you just wrote.
- Source-backed factual claims need citations to source pages or raw paths.
- If sources disagree, preserve the tension. Do not silently replace old claims.
- Prefer small, focused Markdown pages over giant catch-all documents.
- Use ASCII filenames: lowercase, hyphenated slugs, `.md` extension.

## Startup Checklist

Before wiki work:

1. Read this file.
2. Read `wiki/index.md`.
3. Read the latest log entries:

   ```bash
   grep "^## \\[" wiki/log.md | tail -10
   ```

4. Search for existing relevant pages before creating new ones:

   ```bash
   python3 scripts/wiki_search.py "<keyword>"
   ```

5. Inspect the specific source files or wiki pages needed for the task.

## Directory Contract

- `raw/inbox/`: user-dropped sources awaiting ingest.
- `raw/processed/`: optional user-managed archive of ingested sources.
- `raw/assets/`: local images, PDFs extracted from clips, and attachments.
- `wiki/sources/`: one source page per ingested source.
- `wiki/entities/`: people, organizations, projects, places, products.
- `wiki/concepts/`: reusable ideas and definitions.
- `wiki/syntheses/`: higher-level summaries that combine many sources.
- `wiki/comparisons/`: comparison tables and decision analyses.
- `wiki/questions/`: reusable answers created from user queries.
- `wiki/lints/`: periodic health reports.
- `templates/`: copyable page templates.
- `docs/`: workflow documentation for humans.

## Page Schema

Every content page under `wiki/` should begin with YAML frontmatter:

```yaml
---
title: Page Title
type: source | entity | concept | synthesis | comparison | question | lint
status: seed | active | stale | deprecated
created: YYYY-MM-DD
updated: YYYY-MM-DD
source_count: 0
tags: []
---
```

Source pages also include:

```yaml
source_id: src-YYYYMMDD-short-slug
source_url:
source_path:
author:
published:
ingested:
```

Use `source_count` for the number of distinct source pages supporting the page.
Set `status: stale` when newer material appears to supersede a page but the page
has not yet been reconciled.

## Link and Citation Conventions

- Use Obsidian wikilinks for wiki-to-wiki links:
  `[[concepts/llm-wiki|LLM wiki]]`.
- Use Markdown links for external URLs and raw file paths.
- Cite source pages in Evidence sections and near important claims.
- Preferred citation style:
  `Evidence: [[sources/karpathy-llm-wiki-pattern|Karpathy LLM Wiki pattern]]`.
- When quoting sources, keep excerpts short and add your synthesis in your own
  words.

## Ingest Workflow

When the user asks to ingest a source:

1. Identify the source path or URL and assign a source ID:
   `src-YYYYMMDD-short-slug`.
2. Read the source. If it references local images, inspect relevant images from
   `raw/assets/`.
3. Search the existing wiki for related pages.
4. Create or update one page in `wiki/sources/`.
5. Update existing entity, concept, synthesis, comparison, or question pages
   affected by the source.
6. Create new pages only when the concept or entity is likely to recur.
7. Record contradictions in a "Tensions" or "Open Questions" section.
8. Update `wiki/index.md` with new or materially changed pages.
9. Append an entry to `wiki/log.md` using this format:

   ```markdown
   ## [YYYY-MM-DD] ingest | Source title

   - Source: `raw/inbox/file.md` or URL
   - Added: [[sources/source-page]]
   - Updated: [[concepts/example]]
   - Notes: One short sentence.
   ```

10. Run `make check`.
11. Report the changed pages and any unresolved questions.

For large or ambiguous sources, summarize the intended filing plan before
touching many pages.

## Query Workflow

When answering a question:

1. Read `wiki/index.md`.
2. Search the wiki with `scripts/wiki_search.py`.
3. Read the most relevant wiki pages.
4. Read raw sources only when the wiki pages do not contain enough evidence.
5. Answer with citations to wiki pages or source pages.
6. If the answer has durable value, ask whether to file it. If filing is
   requested, create a page under `wiki/questions/`, `wiki/syntheses/`, or
   `wiki/comparisons/`, update the index, append the log, and run `make check`.

## Lint Workflow

Run this when the user asks for a health check or after a large ingest:

1. Run:

   ```bash
   make check
   ```

2. Review:
   - broken links
   - pages missing frontmatter
   - pages missing from `wiki/index.md`
   - orphan pages with no inbound links except the index
   - stale pages
   - contradictions between source-backed claims
   - concepts repeatedly mentioned without a page
   - raw sources that appear unprocessed

3. Create `wiki/lints/YYYY-MM-DD-health-check.md` using
   `templates/lint-report.md`.
4. Apply low-risk repairs directly. For interpretive repairs, list recommended
   changes and ask the user.
5. Update `wiki/index.md`, append `wiki/log.md`, and run `make check`.

## Maintenance Style

- Keep page titles direct and boring.
- Prefer clear sections: Summary, Key Claims, Evidence, Related Pages,
  Tensions, Open Questions.
- Preserve provenance. When in doubt, add a source link.
- Keep one-line index descriptions current.
- Avoid duplicating the same long summary in multiple pages. Link instead.
- Mark uncertainty explicitly with `confidence: low` or an Open Questions item.
- Make small coherent commits when the user asks to commit.

