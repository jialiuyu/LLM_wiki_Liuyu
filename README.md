# LLM Wiki Starter

This repository is a local-first starter for the LLM wiki pattern described by
Andrej Karpathy:

https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

The core setup is intentionally simple:

- `raw/` stores immutable source material.
- `wiki/` stores LLM-maintained Markdown pages.
- `AGENTS.md` is the operating schema for Codex or another coding agent.
- `wiki/index.md` is the content map.
- `wiki/log.md` is the append-only activity log.
- `scripts/` contains dependency-free helper tools for checking and searching.

No vector database or hosted service is required. At personal-wiki scale, the
agent should read `wiki/index.md`, search the Markdown files, then open the
relevant pages and sources.

## Quick Start

1. Open this folder as an Obsidian vault, or browse the Markdown files directly.
2. Drop new sources into `raw/inbox/`.
3. Ask Codex from the repository root:

   ```text
   Ingest raw/inbox/<file> into this LLM wiki. Follow AGENTS.md.
   ```

4. Review the changed wiki pages.
5. Run:

   ```bash
   make check
   ```

6. Commit the changes when the wiki update looks right.

## Repository Map

```text
.
├── AGENTS.md              # Agent operating schema
├── Makefile               # Common local commands
├── raw/
│   ├── inbox/             # New source files
│   ├── processed/         # Optional user-managed archive
│   └── assets/            # Images and downloaded attachments
├── wiki/
│   ├── index.md           # Content-oriented map
│   ├── log.md             # Chronological append-only log
│   ├── overview.md        # Current high-level synthesis
│   ├── sources/           # One page per source
│   ├── concepts/          # Concept pages
│   ├── entities/          # People, orgs, projects, places
│   ├── syntheses/         # Larger synthesized notes
│   ├── comparisons/       # Comparison tables and analyses
│   ├── questions/         # Filed query answers
│   └── lints/             # Periodic wiki health reports
├── templates/             # Page templates
├── scripts/               # Local maintenance tools
└── docs/                  # Human-facing workflow docs
```

## Useful Prompts

```text
Ingest raw/inbox/article.md. Create or update all relevant wiki pages, update
wiki/index.md, append wiki/log.md, and run make check.
```

```text
Answer this using the wiki first, then raw sources only if needed: <question>
If the answer is reusable, file it under wiki/questions/.
```

```text
Run a lint pass. Look for broken links, stale claims, contradictions, orphan
pages, missing source coverage, and concepts that deserve their own pages.
Create a report under wiki/lints/.
```

## Current Seed Content

The starter wiki includes one seed source page summarizing the linked LLM wiki
gist and a few concept pages that define the operating model. These are meant
to be edited as your real domain emerges.

