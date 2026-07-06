---
title: vLLM PagedAttention 发布博客
type: source
status: active
created: 2026-06-23
updated: 2026-06-23
source_count: 1
tags: [vllm, pagedattention, llm-serving, kv-cache]
source_id: src-20260623-vllm-pagedattention-blog
source_url: https://vllm.ai/blog/2023-06-20-vllm
source_path: "raw/inbox/vLLM Easy, Fast, and Cheap LLM Serving with PagedAttention.md"
author: Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Yu, Joey Gonzalez, Hao Zhang, Ion Stoica
published: 2023-06-20
ingested: 2026-06-23
---

# vLLM PagedAttention 发布博客

## 摘要

这篇博客是 vLLM 早期发布文章。它把 vLLM 的性能主张归因于
[[concepts/pagedattention|PagedAttention]]：通过更有效地管理 attention key/value
缓存，减少 [[concepts/kv-cache|KV cache]] 内存浪费，让 serving 系统能够 batch 更多
请求，从而提高吞吐。

原文路径：[raw/inbox/vLLM Easy, Fast, and Cheap LLM Serving with PagedAttention.md](../../raw/inbox/vLLM Easy, Fast, and Cheap LLM Serving with PagedAttention.md)

## 关键观点

- 博客把 LLM serving 的关键瓶颈定位为内存，尤其是 autoregressive decoding 期间
  持续保存在 GPU memory 中的 KV cache。
- 来源称 LLaMA-13B 的单个 sequence KV cache 最高可到 1.7GB，并称既有系统会因
  fragmentation 和 over-reservation 浪费 60% 到 80% 的内存。
- PagedAttention 借鉴操作系统 virtual memory 和 paging，将每个 sequence 的 KV
  cache 拆成固定 token 数的 block；逻辑上连续的 block 可以映射到非连续物理 block。
- 这种设计让内存浪费主要限制在最后一个 block；博客称实践中浪费低于 4%。
- PagedAttention 还通过 block table 支持 KV cache 共享，并用 reference count 和
  Copy-on-Write 处理 parallel sampling 这类共享后分叉的场景。
- 博客报告早期实验中 vLLM 相比 Hugging Face Transformers 最高 24x 吞吐提升，
  相比 Hugging Face TGI 最高 3.5x 吞吐提升；这是博客给定模型、硬件和 ShareGPT
  工作负载下的结果。
- 博客还记录了 LMSYS 将 vLLM 用作 FastChat 后端的应用脉络，并称它帮助 Chatbot
  Arena 以更少 GPU 承载更高流量。

## 有用细节

- 本地剪藏引用了四张图表资产：
  `raw/assets/Pasted image 20260623083938.png`、
  `raw/assets/Pasted image 20260623084001.png`、
  `raw/assets/Pasted image 20260623084017.png`、
  `raw/assets/Pasted image 20260623084026.png`。
- 博客给出一个早期在线 serving 命令：
  `python -m vllm.entrypoints.openai.api_server --model lmsys/vicuna-7b-v1.3`。
  这是 2023 年发布时的示例，后续版本 CLI 可能已经变化。

## 张力

- 博客是发布文章，性能数字来自作者选择的早期实验设置；它适合解释动机和直觉，
  但不能单独代表所有模型、硬件或 vLLM 版本的表现。
- 博客中的安装和命令示例可能已经过时；当前使用方式需要以稳定版文档或 release
  notes 为准。

## 相关页面

- [[entities/vllm|vLLM]]
- [[concepts/pagedattention|PagedAttention]]
- [[concepts/kv-cache|KV cache]]
- [[concepts/llm-serving|LLM serving]]
