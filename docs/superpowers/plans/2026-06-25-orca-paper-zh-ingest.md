# ORCA 论文中文化与摄取实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 `raw/assets/osdi22-yu.pdf` 制作为可阅读的中文 Markdown/PDF，并将论文证据摄取到现有 LLM wiki。

**Architecture:** 英文 PDF 继续作为不可变事实来源。中文 Markdown 是译稿主文件，中文 PDF 由该译稿和从原论文提取的图表生成；wiki 来源页保存论文元数据、核心结论、证据边界和译稿链接，相关概念页与实体页只吸收可复用知识。

**Tech Stack:** Python 3、PyMuPDF/pdfplumber、ReportLab、Poppler、Markdown、仓库内 `scripts/wiki_search.py` 与 `make check`

---

### Task 1: 提取论文结构、正文和图表

**Files:**
- Read: `raw/assets/osdi22-yu.pdf`
- Create: `tmp/pdfs/orca-paper/`
- Create: `output/pdf/orca-figures/`

- [x] 使用 `pdfplumber` 或 `pypdf` 提取 19 页正文，核对标题、作者、章节、公式、表格和参考文献边界。
- [x] 使用 Poppler 渲染论文页面，并按原图号导出正文中的图表到 `output/pdf/orca-figures/`。
- [x] 检查每张图的裁剪范围、清晰度和图号，避免正文、页眉页脚或相邻图注混入。

### Task 2: 编写中文 Markdown 译稿

**Files:**
- Create: `output/pdf/orca-paper-zh.md`

- [x] 翻译摘要、正文、图注、表格标题和致谢，保留 `ORCA`、`iteration-level scheduling`、`selective batching` 等必要英文术语。
- [x] 保留章节结构、公式、表格、实验配置和数值，不逐条翻译参考文献。
- [x] 嵌入 `output/pdf/orca-figures/` 中的图表，并在文首标注这是非官方学习译本。
- [x] 对照英文原文检查章节完整性、图表编号、核心性能数字和结论。

### Task 3: 生成并视觉验证中文 PDF

**Files:**
- Create: `output/pdf/orca-paper-zh.pdf`
- Create: `tmp/pdfs/orca-paper-render/`

- [x] 使用 ReportLab 和可用中文字体排版 Markdown 内容，保持一致的标题、正文、代码、图表和页码样式。
- [x] 用 Poppler 将最终 PDF 全部页面渲染为 PNG。
- [x] 逐页检查中文字体、换页、图表清晰度、表格、公式、页码、裁切和重叠问题，发现问题后重新生成。
- [x] 使用 `pdfinfo` 与文本提取检查 PDF 页数、元数据和中文文本可提取性。

### Task 4: 摄取 ORCA 论文

**Files:**
- Create: `wiki/sources/orca-paper.md`
- Create: `wiki/entities/orca.md`
- Modify: `wiki/concepts/llm-serving.md`
- Modify: `wiki/index.md`
- Modify: `wiki/log.md`

- [x] 创建来源页，记录 OSDI 2022 元数据、中文译稿链接、iteration-level scheduling、selective batching、分布式执行和评测结论。
- [x] 创建 ORCA 实体页，区分论文中的系统设计与 2026 年 serving 系统现状，避免把历史评测外推为当前结论。
- [x] 更新 LLM serving 概念页，把 ORCA 作为 iteration-level scheduling 与连续批处理历史脉络中的来源证据。
- [x] 更新 `wiki/index.md`，追加 `wiki/log.md` 的 ingest 和 maintenance 条目。

### Task 5: 验证仓库和交付物

**Files:**
- Verify: `output/pdf/orca-paper-zh.md`
- Verify: `output/pdf/orca-paper-zh.pdf`
- Verify: `wiki/sources/orca-paper.md`
- Verify: `wiki/entities/orca.md`
- Verify: `wiki/concepts/llm-serving.md`
- Verify: `wiki/index.md`
- Verify: `wiki/log.md`

- [x] 运行 `make check`，预期退出码为 0 且没有 error。
- [x] 运行 `git diff --check`，预期退出码为 0。
- [x] 检查本次变更范围，确认没有修改 `raw/assets/osdi22-yu.pdf` 或覆盖用户已有改动。
- [x] 报告中文译稿、中文 PDF、图表目录、wiki 页面、验证命令和仍需人工确认的翻译边界。
