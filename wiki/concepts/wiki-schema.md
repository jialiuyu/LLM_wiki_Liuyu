---
title: Wiki schema
type: concept
status: seed
created: 2026-06-22
updated: 2026-06-22
source_count: 1
tags: [schema, agents]
---

# Wiki Schema

The wiki schema is the rulebook that turns a general agent into a disciplined
maintainer. In this repository, the schema is `AGENTS.md`.

## What It Defines

- directory roles
- page frontmatter
- link and citation conventions
- ingest workflow
- query workflow
- lint workflow
- index and log requirements
- source immutability rules

## Design Principle

The schema should evolve with the wiki. If recurring maintenance problems show
up, update the schema so future agent sessions inherit the improved workflow.

## Evidence

- [[sources/karpathy-llm-wiki-pattern|Karpathy LLM Wiki pattern]]

## Related Pages

- [[concepts/index-and-log|Index and log]]
- [[concepts/source-backed-answering|Source-backed answering]]

