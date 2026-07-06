---
title: 总览
type: synthesis
status: seed
created: 2026-06-22
updated: 2026-06-23
source_count: 1
tags: [llm-wiki, operations]
---

# 总览

这个仓库实现了一个轻量级 [[concepts/llm-wiki|LLM wiki]]：它是由 agent
维护的 Markdown 知识库，以不可变的 [[concepts/raw-sources|raw 来源]] 为基础，
并由可复用的 [[concepts/wiki-schema|wiki 规范]] 约束。

起始设计遵循
[[sources/karpathy-llm-wiki-pattern|Karpathy 的 LLM Wiki 模式]]：

- 来源放在 `raw/`
- 生成知识放在 `wiki/`
- 操作规则放在 `AGENTS.md`
- `wiki/index.md` 映射内容
- `wiki/log.md` 记录时间线

## 操作模型

用户选择要阅读的资料和重要问题。Agent 通过摄取来源、更新页面、维护链接、
暴露矛盾、归档长期有用的回答来维护知识库。

## 当前范围

这个 starter 有意避免外部基础设施。只要有 Markdown、git、Python 3，以及遵守
`AGENTS.md` 的 agent，仓库就能运作。如果 wiki 增长到 `wiki/index.md` 和简单
搜索不够用的程度，可以添加专门的本地搜索工具，而不必改变页面模型。

## 相关页面

- [[concepts/index-and-log|索引和日志]]
- [[concepts/source-backed-answering|来源支撑的回答]]
- [[concepts/wiki-schema|Wiki 规范]]
