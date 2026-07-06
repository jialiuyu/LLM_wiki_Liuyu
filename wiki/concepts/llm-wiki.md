---
title: LLM wiki
type: concept
status: seed
created: 2026-06-22
updated: 2026-06-23
source_count: 1
tags: [llm-wiki, knowledge-base]
---

# LLM Wiki

LLM wiki 是由 agent 维护的、持久的、相互链接的 Markdown 知识库。它不同于
普通检索，因为 agent 会随时间更新知识结构：新来源可以修订旧摘要、添加链接、
创建概念页，并暴露矛盾。

## 为什么重要

wiki 让有用的综合判断能够积累。回答每个问题时，agent 不必从 raw 文档中
重新发现同一批事实，而可以从已经整理和连接过的页面出发。

## 职责

用户负责：

- 选择来源
- 提出问题
- 审阅重要变更
- 决定哪些内容值得长期保存

Agent 负责：

- 摄取来源
- 更新页面
- 维护链接
- 更新索引和日志
- 运行 lint 检查

## 证据

- [[sources/karpathy-llm-wiki-pattern|Karpathy 的 LLM Wiki 模式]]

## 相关页面

- [[overview|总览]]
- [[concepts/raw-sources|Raw 来源]]
- [[concepts/wiki-schema|Wiki 规范]]
- [[concepts/source-backed-answering|来源支撑的回答]]
