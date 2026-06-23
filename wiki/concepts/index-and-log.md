---
title: Index and log
type: concept
status: seed
created: 2026-06-22
updated: 2026-06-22
source_count: 1
tags: [navigation, logging]
---

# Index And Log

`wiki/index.md` and `wiki/log.md` are the two navigation files that keep the
wiki usable as it grows.

## Index

The index is content-oriented. It lists pages by category with links and
one-line summaries. Agents should read it before answering questions or
ingesting related sources.

## Log

The log is chronological and append-only. It records ingests, queries, lint
passes, schema changes, and maintenance. Consistent headings make it easy to
inspect recent activity with shell tools.

## Evidence

- [[sources/karpathy-llm-wiki-pattern|Karpathy LLM Wiki pattern]]

## Related Pages

- [[concepts/wiki-schema|Wiki schema]]
- [[concepts/llm-wiki|LLM wiki]]

