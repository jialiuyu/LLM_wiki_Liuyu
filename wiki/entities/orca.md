---
title: ORCA
type: entity
status: active
created: 2026-06-25
updated: 2026-06-25
source_count: 2
tags: [orca, llm-serving, transformer, scheduling]
entity_type: project
---

# ORCA

## 摘要

ORCA 是 OSDI 2022 论文提出的分布式 Transformer generative model serving system。
它的核心贡献是 iteration-level scheduling 和 selective batching：让请求在每个
生成 iteration 后重新组成 batch，并允许处于不同阶段或 token position 的请求共同
执行。

## 已知事实

- ORCA 由 Gyeong-In Yu、Joo Seong Jeong、Geon-Woo Kim、Soojeong Kim 和
  Byung-Gon Chun 提出。证据：[[sources/orca-paper|ORCA 论文]]
- ORCA 的 scheduler 每次只让 execution engine 执行一个 iteration，使完成请求可
  及时返回，新请求可在下一轮加入。证据：[[sources/orca-paper|ORCA 论文]]
- Selective batching 对非 Attention operation 做 token-wise batching，对 Attention
  按请求拆分并使用 K/V manager 保存历史状态。证据：[[sources/orca-paper|ORCA 论文]]
- ORCA 组合 intra-layer 与 inter-layer parallelism，并把 control plane 与 GPU data
  plane 分离。证据：[[sources/orca-paper|ORCA 论文]]
- 论文在特定 175B、A100 和合成 workload 条件下，报告 ORCA 相对
  FasterTransformer 在相近延迟水平达到 36.9x 吞吐。证据：
  [[sources/orca-paper|ORCA 论文]]
- SOSP 2023 的 PagedAttention 论文把 ORCA 作为 serving baseline，并报告 vLLM 在其
  实验条件下比 Orca/FasterTransformer 高 2-4x 吞吐。证据：
  [[sources/pagedattention-paper|PagedAttention 论文]]

## 时间线

- 2022-07-11：ORCA 论文发表于 OSDI 2022。
- 2023：PagedAttention 论文将 Orca 作为 LLM serving 对比系统之一。
- 2026-06-25：本 wiki 摄取 ORCA 英文论文并生成中文学习译本。

## 证据

- [[sources/orca-paper|ORCA 论文]]
- [[sources/pagedattention-paper|PagedAttention 论文]]

## 张力

- ORCA 的实验反映 2022 年的硬件、模型和 baseline，不能把论文数字视为当前系统排名。
- ORCA 通过调度和选择性批处理提高执行效率，但其预留式 K/V 状态管理仍留下显存利用率
  优化空间；PagedAttention 从另一个方向解决这一问题。
- ORCA 与后来常说的 continuous batching 存在直接思想联系，但具体系统可能采用不同
  scheduler、prefill/decode 策略和 KV cache manager。

## 相关页面

- [[concepts/llm-serving|LLM serving]]
- [[concepts/kv-cache|KV cache]]
- [[entities/vllm|vLLM]]
- [[concepts/pagedattention|PagedAttention]]
