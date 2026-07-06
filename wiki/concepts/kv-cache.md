---
title: KV cache
type: concept
status: active
created: 2026-06-23
updated: 2026-06-23
source_count: 2
tags: [kv-cache, inference, llm-serving, memory]
---

# KV Cache

## 摘要

KV cache 是 Transformer LLM 在 autoregressive generation 中保存的 attention key
和 value tensor。模型逐 token 生成时，新 token 需要访问前面 token 的 key/value；
缓存这些 tensor 可以避免每一步重复计算全部历史。

在 LLM serving 中，KV cache 是核心工程对象：它大、动态、与 sequence 长度相关，
并且会随请求进入、生成、结束而不断增长和释放。

## 关键点

- prompt phase 可以较好地利用 GPU 并行；autoregressive generation phase 逐 token
  生成，更容易变成 memory-bound。证据：[[sources/pagedattention-paper|PagedAttention 论文]]
- KV cache 大小随请求数量、sequence length、层数、hidden size 和精度增长。论文以
  13B 参数模型为例说明单请求 KV cache 可以达到 GB 级。证据：
  [[sources/pagedattention-paper|PagedAttention 论文]]
- 如果为每个请求预留连续 KV cache 空间，实际输出长度未知会导致 reservation、
  internal fragmentation 和 external fragmentation。证据：
  [[sources/pagedattention-paper|PagedAttention 论文]]
- [[concepts/pagedattention|PagedAttention]] 的核心就是把 KV cache 从连续 tensor
  管理改成 block/page 式管理。证据：
  [[sources/vllm-pagedattention-blog|vLLM PagedAttention 发布博客]]
- complex decoding algorithms 让 KV cache 管理更复杂，但也带来共享机会，例如
  parallel sampling 和 beam search 中公共 prompt 或公共前缀的 KV cache 共享。
  证据：[[sources/pagedattention-paper|PagedAttention 论文]]

## 证据

- [[sources/pagedattention-paper|PagedAttention 论文]]
- [[sources/vllm-pagedattention-blog|vLLM PagedAttention 发布博客]]

## 张力

- 当前页面从 vLLM/PagedAttention 视角解释 KV cache；还没有覆盖其他框架中的 KV
  compression、quantized KV cache、CPU/disk offload、prefix/radix cache 或跨节点
  KV transfer。

## 开放问题

- KV cache 的 block size、eviction、sharing 和 offloading 如何共同影响吞吐与尾延迟？
- 当 serving 目标从单模型转向多模型、多租户或 disaggregated serving 时，KV cache
  管理边界应如何变化？

## 相关页面

- [[concepts/pagedattention|PagedAttention]]
- [[concepts/llm-serving|LLM serving]]
- [[entities/vllm|vLLM]]
