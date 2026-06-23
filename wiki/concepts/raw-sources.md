---
title: Raw sources
type: concept
status: seed
created: 2026-06-22
updated: 2026-06-22
source_count: 1
tags: [sources, provenance]
---

# Raw Sources

Raw sources are the immutable materials the wiki is based on: articles, papers,
notes, images, transcripts, datasets, or other files supplied by the user.

## Rules

- Store source files under `raw/`.
- Do not edit source contents.
- Keep images and attachments local when possible under `raw/assets/`.
- Create a source page under `wiki/sources/` during ingest.
- Cite source pages from concept, entity, synthesis, and answer pages.

## Why It Matters

The wiki can be revised as interpretations improve, but the raw source layer
preserves provenance. This keeps later synthesis auditable.

## Evidence

- [[sources/karpathy-llm-wiki-pattern|Karpathy LLM Wiki pattern]]

## Related Pages

- [[concepts/source-backed-answering|Source-backed answering]]
- [[concepts/wiki-schema|Wiki schema]]

