# AGENTS.md - LLM Wiki 维护规范

本文件是维护本仓库的 agent 操作规范。编辑 wiki 内容前必须先遵守它。

## 使命

维护一个持久、可溯源、以 Markdown 为核心的个人知识 wiki。用户负责选择资料、
设定优先级和审阅结果；agent 负责日常维护工作：总结、归档、链接、修订、
发现矛盾，并保持索引和日志最新。

## 不可破坏的约束

- `raw/` 是事实来源层。不要编辑来源内容。除非用户明确要求，不要把文件移出
  `raw/inbox/`。
- `wiki/` 是 agent 维护层。只要遵守下面的流程，就可以编辑其中内容。
- `AGENTS.md` 是维护规范。wiki 需求变化时先提出规范调整；只有在用户接受或
  明确要求时，才编辑本文件。
- 创建、重命名或实质性修改页面时，必须同步更新 `wiki/index.md`。
- `wiki/log.md` 只能追加。可以修正刚写入条目的明显格式错误，不要改写历史。
- 有来源支撑的事实性陈述需要引用来源页或 `raw/` 路径。
- 如果来源之间有冲突，保留这种张力；不要静默替换旧说法。
- 优先写小而聚焦的 Markdown 页面，避免巨大而含混的汇总文档。
- 文件名使用 ASCII：小写、短横线 slug、`.md` 后缀。

## Codex 维护方式

Codex 在本仓库工作时，默认使用中文、开发者友好的方式维护项目：

- 面向用户的说明、问题回答、维护记录、模板占位文本和 wiki 正文优先使用中文。
- 保留必要的技术标识符、路径、命令、frontmatter 字段、source ID 和文件名为英文
  或 ASCII，避免破坏工具链和 Obsidian 链接。
- 回答要直接说明做了什么、改了哪些页面、有哪些未决问题，以及验证结果。
- 执行维护任务前先读索引和最近日志；不要只凭记忆改页面。
- 能自动验证的事项必须运行 `make check`。如果没有运行成功，要说明原因。
- 对不确定的来源解释要显式标注，不要把推断写成事实。

## 启动清单

开始 wiki 工作前：

1. 阅读本文件。
2. 阅读 `wiki/index.md`。
3. 阅读最近日志条目：

   ```bash
   grep "^## \\[" wiki/log.md | tail -10
   ```

4. 创建新页面前，先搜索已有相关页面：

   ```bash
   python3 scripts/wiki_search.py "<keyword>"
   ```

5. 检查当前任务需要的具体来源文件或 wiki 页面。

以上命令保持英文是为了便于复制执行；实际维护说明和页面正文应优先写中文。

## 目录约定

- `raw/inbox/`: 用户放入、等待摄取的来源。
- `raw/processed/`: 可选的用户管理归档，用于已摄取来源。
- `raw/assets/`: 本地图片、从剪藏中提取的 PDF 和附件。
- `wiki/sources/`: 每个已摄取来源对应一个来源页。
- `wiki/entities/`: 人物、组织、项目、地点、产品。
- `wiki/concepts/`: 可复用概念和定义。
- `wiki/syntheses/`: 跨多个来源的高层综合。
- `wiki/comparisons/`: 对比表和决策分析。
- `wiki/questions/`: 从用户问题沉淀出的可复用回答。
- `wiki/lints/`: 周期性健康检查报告。
- `templates/`: 可复制的页面模板。
- `docs/`: 面向人的工作流文档。

## 页面结构

`wiki/` 下的每个内容页都应该以 YAML frontmatter 开头：

```yaml
---
title: 页面标题
type: source | entity | concept | synthesis | comparison | question | lint
status: seed | active | stale | deprecated
created: YYYY-MM-DD
updated: YYYY-MM-DD
source_count: 0
tags: []
---
```

来源页还要包含：

```yaml
source_id: src-YYYYMMDD-short-slug
source_url:
source_path:
author:
published:
ingested:
```

`source_count` 表示支撑该页面的不同来源页数量。当新材料看起来已经覆盖旧页面、
但尚未完成协调时，把 `status` 标为 `stale`。

## 链接和引用约定

- wiki 内部链接使用 Obsidian wikilink：`[[concepts/llm-wiki|LLM wiki]]`。
- 外部 URL 和 `raw/` 文件路径使用 Markdown 链接。
- 在“证据”章节和重要事实性陈述附近引用来源页。
- 推荐引用格式：`证据：[[sources/karpathy-llm-wiki-pattern|Karpathy 的 LLM Wiki 模式]]`。
- 引用来源时只保留短摘录，并用自己的话写综合判断。

## 摄取流程

用户要求摄取来源时：

1. 识别来源路径或 URL，并分配来源 ID：
   `src-YYYYMMDD-short-slug`.
2. 阅读来源。如果来源引用本地图片，从 `raw/assets/` 检查相关图片。
3. 搜索已有 wiki 页面，找到相关内容。
4. 在 `wiki/sources/` 创建或更新一个来源页。
5. 更新受该来源影响的 entity、concept、synthesis、comparison 或 question 页面。
6. 只有当概念或实体可能反复出现时，才创建新页面。
7. 在“张力”或“开放问题”章节记录矛盾。
8. 用新增或实质性修改的页面更新 `wiki/index.md`。
9. 按下面格式向 `wiki/log.md` 追加条目：

   ```markdown
   ## [YYYY-MM-DD] ingest | 来源标题

   - Source: `raw/inbox/file.md` or URL
   - Added: [[sources/source-page]]
   - Updated: [[concepts/example]]
   - Notes: 一句简短说明。
   ```

10. 运行 `make check`。
11. 报告变更页面和未解决问题。

如果来源很大或含义不明确，先概述归档计划，再批量修改页面。

## 问答流程

回答问题时：

1. 阅读 `wiki/index.md`。
2. 使用 `scripts/wiki_search.py` 搜索 wiki。
3. 阅读最相关的 wiki 页面。
4. 只有当 wiki 页面证据不足时，才阅读 raw 来源。
5. 回答时引用 wiki 页面或来源页。
6. 如果答案具有长期价值，询问是否沉淀进 wiki。用户要求归档时，在
   `wiki/questions/`、`wiki/syntheses/` 或 `wiki/comparisons/` 下创建页面，
   更新索引，追加日志，并运行 `make check`。

## 健康检查流程

用户要求健康检查，或完成大规模摄取后：

1. 运行：

   ```bash
   make check
   ```

2. 检查：
   - 断裂链接
   - 缺少 frontmatter 的页面
   - 没有出现在 `wiki/index.md` 中的页面
   - 除索引外没有入链的孤立页面
   - 标为 stale 的页面
   - 来源支撑的陈述之间是否矛盾
   - 反复出现但还没有独立页面的概念
   - 看起来尚未处理的 raw 来源

3. 使用 `templates/lint-report.md` 创建
   `wiki/lints/YYYY-MM-DD-health-check.md`。
4. 低风险修复可以直接执行。涉及解释或判断的修复，列出建议并询问用户。
5. 更新 `wiki/index.md`，追加 `wiki/log.md`，并运行 `make check`。

## 维护风格

- 页面标题直接、朴素，不追求营销感。
- 优先使用清晰章节：摘要、关键观点、证据、相关页面、张力、开放问题。
- 保留来源脉络。不确定时，添加来源链接。
- 保持索引中的一行说明最新。
- 避免在多个页面复制同一段长摘要；用链接连接。
- 用 `confidence: low` 或开放问题显式标记不确定性。
- 用户要求提交时，使用小而连贯的 commit。
