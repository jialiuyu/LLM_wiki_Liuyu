---
title: LLM serving
type: concept
status: active
created: 2026-06-23
updated: 2026-06-25
source_count: 4
tags: [llm-serving, inference, deployment]
---

# LLM Serving

## 摘要

LLM serving 指把大语言模型作为可调用服务运行的工程层：它不只执行一次推理，
还要处理请求入口、批处理、KV cache 管理、decoding、流式输出、结构化输出、
模型和硬件适配，以及面向应用的 API。

当前定义主要从 ORCA、vLLM 文档首页、PagedAttention 发布博客和 SOSP 2023 论文
归纳而来。

## 关键点

- Serving 系统通常关注吞吐和延迟，而不仅是单次模型调用是否能跑通。
- [[entities/orca|ORCA]] 论文说明，自回归生成的多迭代特性会使 request-level
  scheduling 产生早完成请求阻塞和新请求排队。Iteration-level scheduling 让
  scheduler 每轮重新组成 batch，是 continuous batching 历史脉络中的重要设计。
  证据：[[sources/orca-paper|ORCA 论文]]
- ORCA 的 selective batching 表明，细粒度调度还需要 execution engine 理解不同
  operation 的 batchability：非 Attention operation 可按 token 合并，而 Attention
  需要保留请求边界和各自的 K/V 状态。证据：[[sources/orca-paper|ORCA 论文]]
- vLLM 首页把 PagedAttention、continuous batching、chunked prefill 和 prefix
  caching 放在性能能力中，说明 KV cache 管理和批处理是 LLM serving 的核心工程面。
  证据：[[sources/vllm-docs-home|vLLM 文档首页]]
- PagedAttention 论文把高吞吐 serving 的 batch size 限制明确追溯到
  [[concepts/kv-cache|KV cache]] 的动态增长、碎片化和重复存储。证据：
  [[sources/pagedattention-paper|PagedAttention 论文]]
- [[concepts/pagedattention|PagedAttention]] 的设计说明，LLM serving 的关键优化常常
  发生在模型执行之外的内存布局、调度和共享层。证据：
  [[sources/vllm-pagedattention-blog|vLLM PagedAttention 发布博客]]；
  [[sources/pagedattention-paper|PagedAttention 论文]]
- 面向应用的 serving 需要 API 层和输出协议。vLLM 首页列出 OpenAI-compatible API
  server、Anthropic Messages API、gRPC、streaming outputs、structured outputs、
  tool calling 和 reasoning parsers。证据：[[sources/vllm-docs-home|vLLM 文档首页]]
- Serving 层还需要覆盖模型和硬件差异。vLLM 首页强调 Hugging Face 集成、200+
  模型架构、多种并行方式，以及 NVIDIA、AMD、CPU 和其他硬件插件。
  证据：[[sources/vllm-docs-home|vLLM 文档首页]]

## 证据

- [[sources/orca-paper|ORCA 论文]]
- [[sources/vllm-docs-home|vLLM 文档首页]]
- [[sources/vllm-pagedattention-blog|vLLM PagedAttention 发布博客]]
- [[sources/pagedattention-paper|PagedAttention 论文]]

## 张力

- 当前页面已加入 ORCA 的调度视角，但来源仍集中在 ORCA/vLLM/PagedAttention，
  容易把这些系统边界误当成 LLM serving 的完整分类法；后续应补充其他 serving
  框架、论文、部署实践或 benchmark 来源。
- ORCA 使用 iteration-level scheduling，vLLM 文档使用 continuous batching。
  两者有直接思想联系，但没有更多来源时不应把所有实现细节视为完全等价。

## 开放问题

- vLLM 的 PagedAttention 与其他 serving 系统的 KV cache 管理方案如何对比？
- continuous batching、prefix caching 和 speculative decoding 在不同工作负载下
  各自解决什么瓶颈？

## 相关页面

- [[entities/vllm|vLLM]]
- [[entities/orca|ORCA]]
- [[concepts/pagedattention|PagedAttention]]
- [[concepts/kv-cache|KV cache]]
