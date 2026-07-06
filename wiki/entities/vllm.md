---
title: vLLM
type: entity
status: active
created: 2026-06-23
updated: 2026-06-23
source_count: 3
tags: [vllm, llm-serving, inference]
entity_type: project
---

# vLLM

## 摘要

vLLM 是一个面向 LLM 推理和服务的开源项目。已摄取来源显示，它的早期核心贡献是
用 [[concepts/pagedattention|PagedAttention]] 改善 [[concepts/kv-cache|KV cache]]
内存管理；后续文档则把它扩展为覆盖批处理、量化、优化 kernel、API server、分布式
推理和多模型/多硬件支持的 serving engine。

## 已知事实

- vLLM 把自己定位为用于 LLM inference 和 serving 的快速、易用库。
  证据：[[sources/vllm-docs-home|vLLM 文档首页]]
- 来源称 vLLM 最初由 UC Berkeley Sky Computing Lab 开发，后来由更广泛的学术和
  企业社区维护。证据：[[sources/vllm-docs-home|vLLM 文档首页]]
- 文档首页把 PagedAttention、continuous batching、chunked prefill、prefix
  caching、量化、优化 attention/GEMM/MoE kernel 和 speculative decoding 列为性能
  相关能力。证据：[[sources/vllm-docs-home|vLLM 文档首页]]
- 2023 年发布博客把 vLLM 的吞吐提升主因归结为 PagedAttention 对 KV cache 的分页式
  管理。证据：[[sources/vllm-pagedattention-blog|vLLM PagedAttention 发布博客]]
- SOSP 2023 论文把 vLLM 描述为构建在 PagedAttention 之上的 LLM serving system，
  并报告相对 FasterTransformer 和 Orca 有 2-4x 吞吐提升。证据：
  [[sources/pagedattention-paper|PagedAttention 论文]]
- 文档首页还强调 Hugging Face 集成、OpenAI-compatible API server、Anthropic
  Messages API、gRPC、结构化输出、tool calling、多 LoRA 和多硬件支持。
  证据：[[sources/vllm-docs-home|vLLM 文档首页]]

## 时间线

- 2023-06-20：vLLM 发布博客介绍 PagedAttention 和早期 serving 性能结果。
- 2023-09-12：PagedAttention 论文提交到 arXiv，论文标注为 SOSP 2023。
- 2026-06-23：摄取 vLLM 文档首页、PagedAttention 发布博客和论文 PDF。

## 证据

- [[sources/vllm-docs-home|vLLM 文档首页]]
- [[sources/vllm-pagedattention-blog|vLLM PagedAttention 发布博客]]
- [[sources/pagedattention-paper|PagedAttention 论文]]

## 张力

- 当前页面已有首页、发布博客和论文支撑，但仍缺少 release notes、当前 benchmark、
  生产部署案例，以及与 TGI、SGLang、TensorRT-LLM 等系统的近期对比。

## 相关页面

- [[concepts/llm-serving|LLM serving]]
- [[concepts/pagedattention|PagedAttention]]
- [[concepts/kv-cache|KV cache]]
