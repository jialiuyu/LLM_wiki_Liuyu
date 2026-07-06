---
title: RDMA 基础知识（参考笔记）
type: source
status: active
created: 2026-07-05
updated: 2026-07-05
source_count: 1
tags: [rdma, networking, infiniband, verbs, fundamentals]
source_id: src-20260705-rdma-fundamentals
source_url:
source_path: raw/inbox/rdma-fundamentals.md
author: agent 整理（综合 NVIDIA RDMA Manual、IBTA spec、Netdev RDMA Tutorial、rdma-core）
published:
ingested: 2026-07-05
---

# RDMA 基础知识（参考笔记）

## 摘要

agent 整理的 RDMA 基础参考笔记，落在本仓库 `raw/inbox/rdma-fundamentals.md`。覆盖
DMA→RDMA 的核心直觉、软硬件栈、verbs / libibverbs / librdmacm 分工、PD/MR/QP/CQ/WR/WC
词汇表、one-sided 与 two-sided 语义、RC/UC/UD/DC 连接类型、一次 send/recv 的端到端数据
路径，以及内存注册与 pin。

这是把 [[concepts/rdma|RDMA]] 概念页里「尚未通过 raw 摄取」「缺少第一手 spec」的基础
事实首次落到本地来源层。内容综合下列权威来源、用自己的话重组，长期稳定；具体数值/字段
以原文为准：NVIDIA/Mellanox RDMA Aware Networks Programming User Manual、IBTA
InfiniBand Architecture Specification、Netdev 0x16 RDMA Tutorial（Dreier & Gunthorpe）、
Linux rdma-core（libibverbs/librdmacm）文档。

## 关键观点

- **RDMA 绕过的是远端 CPU 和远端内核协议栈**，不是「绕过本机协议栈」。发起方 RNIC 直接
  操作远端已注册内存；数据路径两端 CPU 都不碰数据本身。
- **verbs 数据路径在用户态**（libibverbs：MR/QP/CQ/post/poll），连接建立用 librdmacm。
  这是 kernel bypass 的关键——数据搬运不进内核。
- **核心对象流水线**：应用把 WR 投到 QP → RNIC 异步执行 → 完成进 CQ → 应用 poll CQ 拿
  WC。MR 注册后返回 lkey（本地用）和 rkey（远端 one-sided 用）。
- **one-sided 与 two-sided 的本质**：one-sided 凭「远端地址 + rkey」直接读写、远端 CPU
  零感知；two-sided 双方都参与、接收方需先 post recv。取舍不是「谁更快」，见
  [[sources/rdma-advanced|进阶笔记]]。
- **连接类型决定可扩展性**：RC 1:1、可靠但 QP 数随对端数线性增长；UD/DC 解耦对端数与
  QP 数。
- **内存必须先 pin + register 成 MR**，注册/注销有开销，是后续 MR cache / ODP 工程化的
  根因。

## 有用细节

- 内存注册为什么必须 pin：RNIC 用 DMA 直接访问，物理页必须驻留内存，否则 DMA 会拿到
  错误数据。
- `RDMA WRITE_WITH_IMM` 是 one-sided 搬运 + 「通知对端发 WC」的混合形式，常被误当成
  two-sided。
- 数据路径不进内核，但管理路径（建连、MR 注册、改 QP）进内核；瓶颈在数据路径，管理路径
  别频繁调用。
- 轮询 `poll_cq`（忙等）延迟最低但烧 CPU；事件 `comp_channel` 省 CPU 但多一次唤醒延迟。

## 张力

- 本文是 agent 综合多份权威来源整理，**非从单一 URL 剪藏**；引用具体数值/字段时应回查
  原文（NVIDIA manual / IBTA spec）。与 [[sources/rdma-design-guidelines|Design
  Guidelines]]、[[sources/gpudirect-rdma|GPUDirect RDMA]] 这类单一来源页性质不同，引用时
  注明「基础参考笔记」而非某篇论文结论。
- one-sided/two-sided 取舍的张力在本文只点到为止，完整争论见
  [[sources/rdma-advanced|进阶笔记]] 与 [[comparisons/rdma-one-sided-vs-two-sided|对比页]]。

## 相关页面

- [[concepts/rdma|RDMA]]
- [[sources/rdma-advanced|RDMA 进阶内容（参考笔记）]]
- [[sources/rdma-design-guidelines|Design Guidelines for High Performance RDMA Systems]]
- [[syntheses/rdma-reading-guide|RDMA 阅读导图]]
