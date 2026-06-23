---
title: LLM wiki
type: concept
status: seed
created: 2026-06-22
updated: 2026-06-22
source_count: 1
tags: [llm-wiki, knowledge-base]
---

# LLM Wiki

An LLM wiki is a persistent, interlinked Markdown knowledge base maintained by
an agent. It differs from ordinary retrieval because the agent updates the
knowledge structure over time: new sources can revise old summaries, add links,
create concept pages, and surface contradictions.

## Why It Matters

The wiki lets useful synthesis accumulate. Instead of rediscovering the same
facts from raw documents during every question, the agent can start from pages
that have already been curated and connected.

## Responsibilities

The user:

- chooses sources
- asks questions
- reviews important changes
- decides what is worth preserving

The agent:

- ingests sources
- updates pages
- maintains links
- updates the index and log
- runs lint checks

## Evidence

- [[sources/karpathy-llm-wiki-pattern|Karpathy LLM Wiki pattern]]

## Related Pages

- [[overview|Overview]]
- [[concepts/raw-sources|Raw sources]]
- [[concepts/wiki-schema|Wiki schema]]
- [[concepts/source-backed-answering|Source-backed answering]]
