---
title: vLLM 文档首页
type: source
status: active
created: 2026-06-23
updated: 2026-06-23
source_count: 1
tags: [vllm, llm-serving, inference]
source_id: src-20260623-vllm-docs-home
source_url: https://docs.vllm.ai/en/latest/
source_path: raw/inbox/vLLM.md
author:
published:
ingested: 2026-06-23
---

# vLLM 文档首页

## 摘要

这个来源是 vLLM 文档首页的剪藏。它把 vLLM 描述为用于 LLM 推理和服务的快速、
易用库，并列出它在吞吐、KV cache 管理、批处理、量化、内核优化、分布式推理、
API 兼容和硬件/模型覆盖方面的能力。

原文路径：[raw/inbox/vLLM.md](../../raw/inbox/vLLM.md)

## 关键观点

- vLLM 面向 LLM inference 和 serving，首页把它定位成“easy, fast, and cheap”
  的服务库。
- 来源称 vLLM 最初由 UC Berkeley 的 Sky Computing Lab 开发，之后发展成由学术
  机构和公司共同维护的活跃开源项目。
- 不同用户入口不同：运行开源模型看 Quickstart，构建应用看 User Guide，参与开发
  看 Developer Guide。
- vLLM 的性能能力包括 PagedAttention、continuous batching、chunked prefill、
  prefix caching、CUDA/HIP graph、量化、优化 attention/GEMM/MoE kernel、
  speculative decoding，以及 prefill/decode/encode 分离。
- vLLM 的易用性和灵活性包括 Hugging Face 模型集成、多种 decoding 算法、分布式
  并行、流式输出、结构化输出、tool calling、reasoning parser、OpenAI-compatible
  API server、Anthropic Messages API、gRPC、多 LoRA，以及多硬件后端支持。
- 来源称 vLLM 支持 200+ Hugging Face 模型架构，覆盖 decoder-only、MoE、混合注意力
  和 state-space、多模态、embedding/retrieval、reward/classification 等模型。

## 有用细节

- 首页链接到 Roadmap、GitHub Releases、PagedAttention 博文、SOSP 2023 paper、
  continuous batching 文章和社区 meetup。
- 这个来源适合做 vLLM 和 LLM serving 的入口索引，但不足以替代专门的安装、部署、
  性能或架构资料。

## 张力

- 这是项目文档首页，很多能力是项目自述；具体性能、部署复杂度和版本差异需要后续
  来源补充。
- 来源使用 `latest` 文档 URL，内容可能随版本漂移；本页只反映 2026-06-23 放入
  `raw/inbox/` 的剪藏内容。

## 相关页面

- [[entities/vllm|vLLM]]
- [[concepts/llm-serving|LLM serving]]
- [[concepts/pagedattention|PagedAttention]]
- [[concepts/kv-cache|KV cache]]
