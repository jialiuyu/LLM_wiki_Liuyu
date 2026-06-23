---
title: Overview
type: synthesis
status: seed
created: 2026-06-22
updated: 2026-06-22
source_count: 1
tags: [llm-wiki, operations]
---

# Overview

This repository implements a lightweight [[concepts/llm-wiki|LLM wiki]]: a
Markdown knowledge base maintained by an agent, grounded in immutable
[[concepts/raw-sources|raw sources]], and governed by a reusable
[[concepts/wiki-schema|wiki schema]].

The starting design follows the pattern in
[[sources/karpathy-llm-wiki-pattern|Karpathy LLM Wiki pattern]]:

- sources live in `raw/`
- generated knowledge lives in `wiki/`
- operating rules live in `AGENTS.md`
- `wiki/index.md` maps the content
- `wiki/log.md` records the chronology

## Operating Model

The user chooses what to read and what questions matter. The agent keeps the
knowledge base maintained by ingesting sources, updating pages, preserving
links, surfacing contradictions, and filing durable answers.

## Current Scope

This starter intentionally avoids external infrastructure. The repository can
work with only Markdown, git, Python 3, and an agent that follows `AGENTS.md`.
If the wiki grows past the point where `wiki/index.md` and simple search are
enough, a dedicated local search tool can be added without changing the page
model.

## Related Pages

- [[concepts/index-and-log|Index and log]]
- [[concepts/source-backed-answering|Source-backed answering]]
- [[concepts/wiki-schema|Wiki schema]]

