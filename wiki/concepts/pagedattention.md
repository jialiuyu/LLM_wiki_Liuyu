---
title: PagedAttention
type: concept
status: active
created: 2026-06-23
updated: 2026-06-23
source_count: 2
tags: [pagedattention, kv-cache, llm-serving, vllm]
---

# PagedAttention

## 摘要

PagedAttention 是 vLLM 提出的 attention/KV cache 管理方法。它借鉴操作系统
virtual memory 和 paging：把每个 sequence 的 [[concepts/kv-cache|KV cache]] 分成
固定 token 数的 block，用 block table 把逻辑 block 映射到非连续的物理 block。

它解决的核心问题不是改变模型架构，而是在 LLM serving 中更有效地使用 GPU memory，
让系统能容纳更大的 batch，并支持复杂 decoding 场景里的 KV cache 共享。

## 关键点

- PagedAttention 的对象是 KV cache，而不是模型权重或 prompt 文本本身。
- 传统连续 KV cache 分配会受到 reservation、internal fragmentation 和 external
  fragmentation 影响。证据：[[sources/pagedattention-paper|PagedAttention 论文]]
- PagedAttention 使用固定大小 block 按需分配，物理 block 不需要连续。证据：
  [[sources/vllm-pagedattention-blog|vLLM PagedAttention 发布博客]]；
  [[sources/pagedattention-paper|PagedAttention 论文]]
- block table 是逻辑连续性和物理非连续性的连接层：attention kernel 根据 block
  table 读取 KV cache。证据：[[sources/pagedattention-paper|PagedAttention 论文]]
- 对 parallel sampling、beam search 等场景，多个 sequence 可以共享公共前缀的
  physical blocks，并通过 reference count 和 Copy-on-Write 在分叉时保持正确性。
  证据：[[sources/vllm-pagedattention-blog|vLLM PagedAttention 发布博客]]；
  [[sources/pagedattention-paper|PagedAttention 论文]]
- 论文和博客都把 PagedAttention 视为 vLLM 早期吞吐提升的核心机制。

## 证据

- [[sources/vllm-pagedattention-blog|vLLM PagedAttention 发布博客]]
- [[sources/pagedattention-paper|PagedAttention 论文]]

## 张力

- PagedAttention 解释了 vLLM 早期相对连续 KV cache 管理系统的优势，但现代 serving
  系统可能已经采用其他 KV cache 管理、prefix cache、disaggregated serving 或
  offloading 机制；横向比较需要更多来源。
- PagedAttention 改善 memory management，不自动解决所有 serving 问题，例如调度
  策略、kernel 性能、网络通信、模型加载和多租户隔离。

## 开放问题

- PagedAttention 与 SGLang radix cache、TensorRT-LLM KV cache 管理、TGI 当前实现
  的边界分别是什么？
- 在长上下文、MoE、speculative decoding 和 disaggregated prefill/decode 中，
  block 粒度和 eviction 策略如何影响尾延迟？

## 相关页面

- [[concepts/kv-cache|KV cache]]
- [[entities/vllm|vLLM]]
- [[concepts/llm-serving|LLM serving]]
