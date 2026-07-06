---
title: GPUDirect RDMA 官方文档
type: source
status: active
created: 2026-07-03
updated: 2026-07-03
source_count: 1
tags: [rdma, gpu, nvidia, gpudirect, networking]
source_id: src-20260703-gpudirect-rdma
source_url: https://docs.nvidia.com/cuda/gpudirect-rdma/
source_path:
author: NVIDIA
published:
ingested: 2026-07-03
---

# GPUDirect RDMA 官方文档

## 摘要

NVIDIA 官方文档，介绍 GPUDirect RDMA：一种让第三方 peer 设备（如 RDMA NIC）与 GPU
之间建立直接数据通路、绕过主机内存的技术。从 Kepler 级 GPU 和 CUDA 5.0 起引入，是
分布式 GPU / LLM 通信的关键底层能力。

原文：[GPUDirect RDMA 官方文档](https://docs.nvidia.com/cuda/gpudirect-rdma/)。

注意：本页为外部官方文档，未放入 `raw/`，作为权威背景资料纳入。

## 关键观点

- GPUDirect RDMA 让 RNIC 直接读写 GPU 显存，数据不必在主机 DRAM 中转，省一次拷贝并
  降低延迟与 CPU 占用。
- 实现依赖 NVIDIA 驱动加 peer-to-peer 内核模块（现名 `nvidia-peermem`，旧名
  `nv_peer_memory`）。
- 拿到真正 PCIe P2P 直连通常要求 NIC 与 GPU 在同一 PCIe root complex（NUMA 亲和）；
  跨 socket 或跨 PCIe switch 会退化为经主机内存中转，失去主要收益。
- 与 NCCL 结合时，这是跨节点 allreduce 等集合通信走 RDMA 的基础；NCCL 通过 transport
  plugin 调用 GPUDirect RDMA 搬运 GPU 张量。
- GPUDirect 还包括 Shared Memory、P2P、Storage、Video 等其他子能力，本页聚焦 RDMA
  方向。

## 有用细节

- 文档涵盖设计原理、设置步骤、编程指南和已知限制，是排查“GPUDirect RDMA 没生效”问题
  的第一手参考。
- 典型故障：peermem 模块未加载、NIC 与 GPU 不在同一 NUMA、容器（PCIe / CUDA / GID）
  权限不足，都会让 GPUDirect RDMA 静默退回 bounce-buffer。

## 张力

- 这是厂商（NVIDIA）文档，描述自家产品时偏向正面；对局限（如 NUMA 退化、与某些 NIC /
  驱动组合的兼容问题）描述偏保守，应配合社区排错经验（NCCL forum、vLLM 多节点部署
  讨论）。
- `nvidia-peermem` 与旧 `nv_peer_memory` 的迁移、与不同内核 / CUDA 版本的兼容性会随
  时间变化，具体以当前 NVIDIA 文档为准。

## 相关页面

- [[concepts/rdma|RDMA]]
- [[concepts/llm-serving|LLM serving]]
- [[syntheses/rdma-reading-guide|RDMA 阅读导图]]
