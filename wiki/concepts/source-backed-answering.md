---
title: Source-backed answering
type: concept
status: seed
created: 2026-06-22
updated: 2026-06-22
source_count: 1
tags: [query, citations]
---

# Source-Backed Answering

Source-backed answering means the agent answers questions by starting from the
wiki, reading source pages and raw sources when needed, and preserving citations
for important claims.

## Workflow

1. Read `wiki/index.md`.
2. Search the wiki for relevant pages.
3. Open the strongest related pages.
4. Open raw sources only when the wiki lacks enough evidence.
5. Answer with citations.
6. File durable answers into the wiki when useful.

## Why It Matters

Answers should compound into the knowledge base. A useful comparison, synthesis,
or explanation should not disappear into chat history if it will help future
questions.

## Evidence

- [[sources/karpathy-llm-wiki-pattern|Karpathy LLM Wiki pattern]]

## Related Pages

- [[concepts/index-and-log|Index and log]]
- [[concepts/raw-sources|Raw sources]]

