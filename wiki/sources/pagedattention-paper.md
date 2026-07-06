---
title: PagedAttention 论文
type: source
status: active
created: 2026-06-23
updated: 2026-06-23
source_count: 1
tags: [pagedattention, vllm, llm-serving, kv-cache, paper]
source_id: src-20260623-pagedattention-paper
source_url: https://arxiv.org/abs/2309.06180
source_path: raw/assets/PagedAttention.pdf
author: Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph E. Gonzalez, Hao Zhang, Ion Stoica
published: 2023-09-12
ingested: 2026-06-23
---

# PagedAttention 论文

## 摘要

这篇 SOSP 2023 论文系统化阐述了 [[concepts/pagedattention|PagedAttention]]
和 vLLM。论文的问题定义是：高吞吐 LLM serving 需要足够大的 batch，但每个请求的
[[concepts/kv-cache|KV cache]] 很大、动态增长收缩，并且在连续内存管理下容易产生
fragmentation 和重复存储，最终限制 batch size。

原文路径：[raw/assets/PagedAttention.pdf](../../raw/assets/PagedAttention.pdf)

## 中文译稿与图版

- [中文 Markdown 译稿](../../output/pdf/pagedattention-paper-zh.md)
- [中文 PDF 阅读版](../../output/pdf/pagedattention-paper-zh.pdf)
- 论文图 1-19 已单独导出到
  `output/pdf/pagedattention-figures/`，并按原图号嵌入上述译稿。

译稿保留正文结构、公式、表格、图注和实验数字；参考文献条目未逐条翻译。
这是非官方学习译本，引用论文结论时仍应以英文原文为准。

## 关键观点

- 论文把 LLM serving 的吞吐瓶颈归因于 KV cache memory management，而不只是模型
  计算本身。
- 在 13B 参数模型的 A100 40GB 示例中，模型权重约占 65% GPU memory，KV cache
  可占接近 30%；因此 KV cache 管理方式会直接影响可容纳的 batch size。
- 既有系统倾向于为每个请求预留连续 KV cache tensor，导致 reservation、internal
  fragmentation 和 external fragmentation。
- PagedAttention 以固定大小 block 管理 KV cache；逻辑 block 和物理 block 通过
  block table 映射，物理 block 不要求连续。
- 这种 paging 式设计通过按需分配降低 internal fragmentation，通过同尺寸 block
  消除 external fragmentation，并支持 block 粒度的跨 sequence 或跨 request 共享。
- vLLM 在 PagedAttention 之上实现了分布式 LLM serving engine，包括 block-level
  memory management、preemptive request scheduling、KV cache manager 和 worker
  侧 cache engine。
- 论文报告 vLLM 相比 FasterTransformer 和 Orca 在相同 latency 水平下有 2-4x
  吞吐提升；提升在长序列、大模型和复杂 decoding 算法下更明显。

## 有用细节

- 论文明确区分 prompt phase 和 autoregressive generation phase：前者可以并行化，
  后者逐 token 生成，通常更 memory-bound。
- 对 parallel sampling 和 beam search，论文把共享机会归结为多个输出或 beam 之间
  的公共前缀 KV cache；PagedAttention 用 reference count 和 Copy-on-Write 支持这种
  共享。
- 论文还讨论了未知输入/输出长度下的 scheduling，包括当 GPU memory 不足时删除或
  swapping KV block 的策略。

## 张力

- 论文评测是 2023 年语境下对 FasterTransformer、Orca 等系统的比较；不能直接外推
  到 2026 年的 vLLM、TGI、SGLang、TensorRT-LLM 或生产部署形态。
- 论文证明的是 PagedAttention/vLLM 在特定模型和工作负载下的 memory management
  优势，不等同于所有 serving 场景都由 KV cache 瓶颈主导。

## 相关页面

- [[concepts/pagedattention|PagedAttention]]
- [[concepts/kv-cache|KV cache]]
- [[entities/vllm|vLLM]]
- [[concepts/llm-serving|LLM serving]]
