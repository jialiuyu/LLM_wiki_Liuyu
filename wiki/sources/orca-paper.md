---
title: ORCA 论文
type: source
status: active
created: 2026-06-25
updated: 2026-06-25
source_count: 1
tags: [orca, llm-serving, scheduling, batching, transformer, paper]
source_id: src-20260625-orca-paper
source_url: https://www.usenix.org/conference/osdi22/presentation/yu
source_path: raw/assets/osdi22-yu.pdf
author: Gyeong-In Yu, Joo Seong Jeong, Geon-Woo Kim, Soojeong Kim, Byung-Gon Chun
published: 2022-07-11
ingested: 2026-06-25
---

# ORCA 论文

## 摘要

这篇 OSDI 2022 论文提出 [[entities/orca|ORCA]]，一个面向自回归 Transformer
生成模型的分布式 serving system。论文识别出 request-level scheduling 与生成式
模型多迭代执行之间的错配，并提出 iteration-level scheduling 和 selective batching。

原文路径：[raw/assets/osdi22-yu.pdf](../../raw/assets/osdi22-yu.pdf)

## 中文译稿与图版

- [中文 Markdown 译稿](../../output/pdf/orca-paper-zh.md)
- [中文 PDF 阅读版](../../output/pdf/orca-paper-zh.pdf)
- 论文图 1-11、算法 1 和表 1 已导出到 `output/pdf/orca-figures/`，并按原编号嵌入译稿。

译稿保留正文结构、算法、表格、图注和实验数字；参考文献条目未逐条翻译。
这是非官方学习译本，引用论文结论时仍应以英文原文为准。

## 关键观点

- 传统 serving system 与 execution engine 通常按整个请求或 batch 交互。生成请求需要
  多轮执行且完成时间不同，因此早完成请求不能及时返回，新请求也不能在当前 batch
  运行期间加入。
- Iteration-level scheduling 让 scheduler 每次只调用 execution engine 执行一个
  iteration，并在每轮结束后重新选择请求。
- 任意请求集合可能处于不同 phase 或 token position，Attention key/value tensor
  shape 不同，无法直接使用传统规则 batch。
- Selective batching 对 Linear、LayerNorm、GeLU、Add 等 operation 做 token-wise
  batching，但在 Attention 前按请求 Split，分别计算后再 Merge。
- ORCA 将 control plane 与 data plane 分离：CPU control message 使用 gRPC 等 channel，
  GPU intermediate tensor 使用 NCCL，以减少每轮 CPU-GPU synchronization。
- 调度算法提供 iteration-level FCFS，并根据每个请求的 `max_tokens` 预留 Attention
  K/V slot，避免请求执行中途因状态空间耗尽而死锁。
- ORCA 利用 iteration 作为跨 worker pipeline 的单位，不必像 FasterTransformer
  一样把 request-level batch 再切为 microbatch。

## 有用细节

- 实现约 13K 行 C++，使用 CUDA、gRPC 和 NCCL，并包含 LayerNorm、Attention、GeLU
  等 fused kernel。
- 评测使用 A100 40GB GPU 和 13B、101B、175B、341B GPT 配置；请求 trace 为合成数据，
  到达时间按 Poisson process 生成。
- 在 engine microbenchmark 中，13B 和 101B 上 ORCA 与 FasterTransformer 性能接近；
  175B 且关闭双方 pipeline 时，ORCA engine 最多快 47%。
- End-to-end 实验中，论文报告 175B 模型在约 190ms median normalized latency 下，
  FasterTransformer 为 0.185 req/s，ORCA 为 6.81 req/s，即 36.9x。
- 论文把 Attention 视为适合按请求拆分的 operation，因为 Attention 本身没有模型参数，
  不会从跨请求复用模型参数读取中获得主要 batching 收益。

## 张力

- 评测基于 2022 年的 FasterTransformer、A100 40GB、GPT 配置和合成请求 trace；
  36.9x 不能直接外推到当前 vLLM、SGLang、TensorRT-LLM 或真实生产 workload。
- ORCA 按 `max_tokens` 为每个请求预留 K/V slot，避免执行中途耗尽，但仍可能产生
  reservation 浪费。后续 [[sources/pagedattention-paper|PagedAttention 论文]]
  将这种连续或预留式 KV cache 管理作为进一步优化对象。
- ORCA 的 scheduler 与 execution engine 紧密集成。论文承认，它没有解决如何在保留
  通用 serving/execution 抽象边界的同时支持两项技术。
- ORCA 论文使用 iteration-level scheduling 描述其机制；后来行业常用的 continuous
  batching 与它密切相关，但术语和具体实现边界不能在没有额外来源时完全等同。

## 相关页面

- [[entities/orca|ORCA]]
- [[concepts/llm-serving|LLM serving]]
- [[concepts/kv-cache|KV cache]]
- [[entities/vllm|vLLM]]
- [[sources/pagedattention-paper|PagedAttention 论文]]
