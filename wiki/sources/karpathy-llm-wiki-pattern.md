---
title: Karpathy 的 LLM Wiki 模式
type: source
status: seed
created: 2026-06-22
updated: 2026-06-23
source_count: 1
tags: [llm-wiki, knowledge-base, obsidian]
source_id: src-20260622-karpathy-llm-wiki-pattern
source_url: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
source_path:
author: Andrej Karpathy
published: 2026-04-04
ingested: 2026-06-22
---

# Karpathy 的 LLM Wiki 模式

## 摘要

这个来源提出了一种由 LLM agent 维护的持久 Markdown wiki。Wiki 位于 raw
文档和后续问题之间，让有用的综合判断先被整理出来，再随着时间维护和复用；
回答每个问题时不必都从 raw 来源重新构建。

## 关键观点

- Wiki 可以成为会复利的产物：每个来源都能更新已有页面、链接、摘要和矛盾。
- 人类负责来源选择、方向设定和审阅。
- Agent 负责总结、归档、交叉链接、记录和常规维护。
- 一个起步系统只需要三层：
  [[concepts/raw-sources|raw 来源]]、生成的 wiki 页面，以及操作
  [[concepts/wiki-schema|规范]]。
- 早期有两个特殊文件很重要：
  [[concepts/index-and-log|索引和日志]]。
- 可选搜索工具可以之后再加；在中等个人 wiki 规模下，精心维护的索引已经足够。

## 对本仓库的意义

本仓库把这个模式实例化到 Codex 和 Obsidian：

- `AGENTS.md` 是规范。
- `raw/` 是不可变来源层。
- `wiki/` 是生成知识层。
- `scripts/wiki_check.py` 实现第一版 lint 检查。
- `scripts/wiki_search.py` 给 agent 一个简单的本地搜索原语。

## 相关页面

- [[concepts/llm-wiki|LLM wiki]]
- [[concepts/wiki-schema|Wiki 规范]]
- [[concepts/source-backed-answering|来源支撑的回答]]
