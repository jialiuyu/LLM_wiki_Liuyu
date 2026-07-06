---
title: Raw 来源
type: concept
status: seed
created: 2026-06-22
updated: 2026-06-23
source_count: 1
tags: [sources, provenance]
---

# Raw 来源

Raw 来源是 wiki 的不可变基础材料：文章、论文、笔记、图片、转录、数据集，
或用户提供的其他文件。

## 规则

- 来源文件存放在 `raw/` 下。
- 不要编辑来源内容。
- 图片和附件尽量本地保存到 `raw/assets/`。
- 摄取时在 `wiki/sources/` 下创建来源页。
- 在概念、实体、综合和回答页面中引用来源页。

## 为什么重要

解释可以随着理解加深而修订，但 raw 来源层保留来源脉络。这让之后的综合判断
仍然可审计。

## 证据

- [[sources/karpathy-llm-wiki-pattern|Karpathy 的 LLM Wiki 模式]]

## 相关页面

- [[concepts/source-backed-answering|来源支撑的回答]]
- [[concepts/wiki-schema|Wiki 规范]]
