# Wiki 日志

摄取、问答、lint、规范变更和维护动作的只追加时间线。条目应以
`## [YYYY-MM-DD] kind | Title` 开头，便于简单工具解析。

## [2026-06-22] schema | 初始化 LLM wiki starter

- Source: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- Added: [[sources/karpathy-llm-wiki-pattern]], [[concepts/llm-wiki]], [[concepts/raw-sources]], [[concepts/wiki-schema]], [[concepts/index-and-log]], [[concepts/source-backed-answering]]
- Notes: 创建初始 raw/wiki/schema 结构、模板和本地检查。

## [2026-06-23] schema | 中文化维护界面和 Codex 规范

- Source: 用户要求将项目主要维护内容改为中文，并为 Codex 配置中文开发者友好的维护方式。
- Updated: [[overview]], [[sources/karpathy-llm-wiki-pattern]], [[concepts/llm-wiki]], [[concepts/raw-sources]], [[concepts/wiki-schema]], [[concepts/index-and-log]], [[concepts/source-backed-answering]]
- Notes: 中文化维护规范、项目说明、模板、索引、日志和现有 wiki 页面；保留 raw 来源内容不变。

## [2026-06-23] ingest | Obsidian Web Clipper Reader

- Source: `raw/inbox/Reader.md`
- Added: [[sources/obsidian-web-clipper-reader]], [[entities/obsidian-web-clipper]]
- Updated: [[wiki/index]]
- Notes: 摄取 Reader 模式帮助页，记录其网页阅读视图、入口和可配置项。

## [2026-06-23] ingest | vLLM 文档首页

- Source: `raw/inbox/vLLM.md`
- Added: [[sources/vllm-docs-home]], [[entities/vllm]], [[concepts/llm-serving]]
- Updated: [[wiki/index]]
- Notes: 摄取 vLLM 首页，沉淀 LLM serving 的初始概念页并标注当前只有一个来源支撑。

## [2026-06-23] ingest | vLLM PagedAttention 发布博客

- Source: `raw/inbox/vLLM Easy, Fast, and Cheap LLM Serving with PagedAttention.md`
- Added: [[sources/vllm-pagedattention-blog]], [[concepts/pagedattention]], [[concepts/kv-cache]]
- Updated: [[entities/vllm]], [[concepts/llm-serving]], [[sources/vllm-docs-home]], [[wiki/index]]
- Notes: 摄取 vLLM 早期发布博客，补充 PagedAttention 的内存管理直觉、性能主张和本地图表附件。

## [2026-06-23] ingest | PagedAttention 论文

- Source: `raw/assets/PagedAttention.pdf`
- Added: [[sources/pagedattention-paper]]
- Updated: [[concepts/pagedattention]], [[concepts/kv-cache]], [[entities/vllm]], [[concepts/llm-serving]], [[wiki/index]]
- Notes: 摄取 SOSP 2023 论文，补充 KV cache 瓶颈、block table、Copy-on-Write、调度和 2-4x 吞吐评测结论。

## [2026-06-23] maintenance | PagedAttention 论文中文译稿与图版

- Source: `raw/assets/PagedAttention.pdf`
- Added: [中文 Markdown 译稿](../output/pdf/pagedattention-paper-zh.md), [中文 PDF 阅读版](../output/pdf/pagedattention-paper-zh.pdf), `output/pdf/pagedattention-figures/`
- Updated: [[sources/pagedattention-paper]], [[wiki/index]]
- Notes: 完成正文中文学习译稿，保留公式、表格和实验数字，并从论文源文件导出图 1-19；中文 PDF 共 19 页。

## [2026-06-25] ingest | ORCA 论文

- Source: `raw/assets/osdi22-yu.pdf`
- Added: [[sources/orca-paper]], [[entities/orca]]
- Updated: [[concepts/llm-serving]], [[wiki/index]]
- Notes: 摄取 OSDI 2022 ORCA 论文，记录 iteration-level scheduling、selective batching、分布式架构、调度算法和论文评测边界。

## [2026-06-25] maintenance | ORCA 论文中文译稿与图版

- Source: `raw/assets/osdi22-yu.pdf`
- Added: [中文 Markdown 译稿](../output/pdf/orca-paper-zh.md), [中文 PDF 阅读版](../output/pdf/orca-paper-zh.pdf), `output/pdf/orca-figures/`
- Updated: [[sources/orca-paper]], [[wiki/index]]
- Notes: 完成 ORCA 正文中文学习译稿，保留图 1-11、算法 1、表 1 和实验数字；中文 PDF 共 17 页。

## [2026-06-27] ingest | C/C++ 程序员的内存模型

- Source: `raw/assets/1803.04432v1.pdf`
- Added: [[sources/cpp-memory-models-programmers]], [[concepts/memory-model]], [[concepts/cpp-memory-ordering]]
- Updated: [[wiki/index]]
- Notes: 摄取 2018 年 C/C++ memory model 教学笔记，沉淀语言/硬件内存模型、weak memory model、C++11 atomics、memory_order 和 fence 的基本脉络。

## [2026-06-28] maintenance | 清理重复 C/C++ memory model PDF

- Source: `raw/assets/1803.04432v1.pdf`
- Removed: `raw/assets/1803.04432v1 (1).pdf`
- Updated: [[sources/cpp-memory-models-programmers]]
- Notes: 两个 PDF 的 SHA-256 均为 `98e11f364881f583fcf09ae4189348e958ae5e8123f527e461543d47fecf47a5`，删除未被来源页引用的重复副本。

## [2026-06-29] maintenance | C/C++ memory model 论文中文译稿与图版

- Source: `raw/assets/1803.04432v1.pdf`
- Added: [中文 Markdown 译稿](../output/pdf/cpp-memory-models-programmers-zh.md), [中文 PDF 阅读版](../output/pdf/cpp-memory-models-programmers-zh.pdf), `output/pdf/cpp-memory-models-figures/`
- Updated: [[sources/cpp-memory-models-programmers]], [[wiki/index]]
- Notes: 完成 C/C++ memory model 正文中文学习译稿，保留代码 listing、图 1-2 和关键 C++ memory_order 术语；中文 PDF 共 11 页。

## [2026-06-29] maintenance | C/C++ 内存模型阅读导图

- Source: `raw/assets/1803.04432v1.pdf`
- Added: [[syntheses/cpp-memory-models-reading-guide]]
- Updated: [[sources/cpp-memory-models-programmers]], [[wiki/index]]
- Notes: 针对逐句译稿难以形成认识的问题，补充结构化导读，按发布例子、硬件模型、C++ 标准术语和 memory_order 选择规则重组知识。

## [2026-06-29] query | relaxed、release/acquire 和 seq_cst 怎么区分

- Source: `raw/assets/1803.04432v1.pdf`
- Added: [[questions/cpp-memory-ordering-relaxed-seqcst]]
- Updated: [[concepts/cpp-memory-ordering]], [[syntheses/cpp-memory-models-reading-guide]], [[wiki/index]]
- Notes: 归档关于 `relaxed` 解决什么、acquire 读到旧值为何没有接住 release、以及 `seq_cst` 如何排除双旧值结果的追问和例子。

## [2026-07-01] query | ORCA 论文里的 CUDA kernel 是什么意思

- Source: `raw/assets/osdi22-yu.pdf`; NVIDIA CUDA 官方文档
- Added: [[questions/cuda-kernel-in-orca]]
- Updated: [[wiki/index]]
- Notes: 归档关于 ORCA fused CUDA kernel、selective batching 和 CUDA/GPU 基础学习路线的回答；CUDA 基础部分作为官方背景资料处理。

## [2026-07-03] maintenance | RDMA 概念页与阅读导图

- Added: [[concepts/rdma]], [[syntheses/rdma-reading-guide]]
- Updated: [[wiki/index]]
- Notes: 补充 RDMA 入门到进阶读物分级推荐；外部链接经 WebSearch 核对。RDMA 资源尚未
  通过 raw 摄取建立来源页，暂以外部权威文档（NVIDIA/Mellanox、USENIX 论文、IBTA）为准，
  并保留 one-sided/two-sided 取舍的张力。

## [2026-07-03] ingest | Design Guidelines 与 GPUDirect RDMA 来源页

- Source: https://www.usenix.org/system/files/conference/atc16/atc16_paper-kalia.pdf ;
  https://docs.nvidia.com/cuda/gpudirect-rdma/
- Added: [[sources/rdma-design-guidelines]], [[sources/gpudirect-rdma]]
- Updated: [[concepts/rdma]], [[syntheses/rdma-reading-guide]], [[wiki/index]]
- Notes: 把 RDMA 两篇核心资料升级为来源页（外部公开来源，未放入 raw，作为权威背景资料，
  与 ORCA 中 CUDA 官方资料处理一致）；概念页 source_count 0→2 并回填证据引用；保留
  one-sided/two-sided 取舍的张力。

## [2026-07-05] maintenance | 推送到 GitHub 公开托管

- Remote: https://github.com/jialiuyu/LLM_wiki_Liuyu (public)
- Updated: `.gitignore`（新增 `output/`）
- Notes: 仓库此前已是 git 仓库但无远程；本次配置 `origin` 并首次推送 `main`。
  将累积未提交改动合并为单个 commit (`58c417e`)；通过 `gh` CLI 创建公开仓库并
  完成 HTTPS 授权。`CLAUDE.md` 在仓库中为指向 `AGENTS.md` 的符号链接。
