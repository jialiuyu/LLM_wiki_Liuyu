---
title: Karpathy LLM Wiki pattern
type: source
status: seed
created: 2026-06-22
updated: 2026-06-22
source_count: 1
tags: [llm-wiki, knowledge-base, obsidian]
source_id: src-20260622-karpathy-llm-wiki-pattern
source_url: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
source_path:
author: Andrej Karpathy
published: 2026-04-04
ingested: 2026-06-22
---

# Karpathy LLM Wiki Pattern

## Summary

This source proposes a persistent Markdown wiki maintained by an LLM agent. The
wiki sits between raw documents and later questions, so useful synthesis is
compiled once, maintained over time, and reused instead of being reconstructed
from raw sources on every query.

## Key Claims

- A wiki can act as a compounding artifact: each source can update existing
  pages, links, summaries, and contradictions.
- The human owns source selection, direction, and review.
- The agent owns summarizing, filing, cross-linking, bookkeeping, and routine
  maintenance.
- Three layers are sufficient for a starter system:
  [[concepts/raw-sources|raw sources]], generated wiki pages, and an operating
  [[concepts/wiki-schema|schema]].
- Two special files matter early:
  [[concepts/index-and-log|index and log]].
- Optional search tooling can be added later, but a carefully maintained index
  can cover moderate personal-wiki scale.

## Relevance To This Repository

This repository instantiates the pattern for Codex and Obsidian:

- `AGENTS.md` is the schema.
- `raw/` is the immutable source layer.
- `wiki/` is the generated knowledge layer.
- `scripts/wiki_check.py` implements a first lint pass.
- `scripts/wiki_search.py` gives the agent a simple local search primitive.

## Related Pages

- [[concepts/llm-wiki|LLM wiki]]
- [[concepts/wiki-schema|Wiki schema]]
- [[concepts/source-backed-answering|Source-backed answering]]

