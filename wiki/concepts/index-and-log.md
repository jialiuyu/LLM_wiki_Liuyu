---
title: 索引和日志
type: concept
status: seed
created: 2026-06-22
updated: 2026-06-23
source_count: 1
tags: [navigation, logging]
---

# 索引和日志

`wiki/index.md` 和 `wiki/log.md` 是两个导航文件，负责让 wiki 在增长过程中
仍然可用。

## 索引

索引面向内容。它按类别列出页面、链接和一行摘要。Agent 在回答问题或摄取
相关来源前，应该先阅读索引。

## 日志

日志按时间排列，只能追加。它记录摄取、问答、lint、规范变更和维护动作。
稳定的标题格式让 shell 工具能快速查看最近活动。

## 证据

- [[sources/karpathy-llm-wiki-pattern|Karpathy 的 LLM Wiki 模式]]

## 相关页面

- [[concepts/wiki-schema|Wiki 规范]]
- [[concepts/llm-wiki|LLM wiki]]
