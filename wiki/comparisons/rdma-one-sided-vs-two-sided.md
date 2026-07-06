---
title: "RDMA: one-sided vs two-sided"
type: comparison
status: active
created: 2026-07-05
updated: 2026-07-05
source_count: 2
tags: [rdma, networking, comparison, design-tradeoff]
---

# RDMA: one-sided vs two-sided

## 摘要

RDMA 的两类核心操作怎么选。结论是**没有「永远更好」的一种**：

- **one-sided（RDMA read / write）**：发起方凭「远端地址 + rkey」直接读写远端内存，
  远端 CPU 零参与。**大块纯搬运、远端不希望被打扰时**占优。
- **two-sided（send / recv）**：双方都参与，接收方在自己已热缓存的 buffer 上处理。
  **小消息、需要远端逻辑或远端 cache 局部性、连接数多时**常胜出。

FaRM（one-sided 派）与 FaSST / HERD（two-sided 派）是真实的研究分歧，Design Guidelines
给出「取决于负载」的工程结论。本页保留这种张力，给出按场景的决策。

## 对比表

| 维度 | one-sided（read/write） | two-sided（send/recv） | 证据 |
| --- | --- | --- | --- |
| 远端 CPU 参与 | 完全不参与，零开销 | 必须先 post recv、收 WC 处理 | 基础笔记 |
| 远端逻辑 / 请求路由 | 无：远端不感知，无法插队或服务端处理 | 有：接收方可在 recv 后执行任意逻辑 | 进阶笔记 |
| 远端 cache 局部性 | 差：数据进 NIC 指定的 MR，与远端 CPU 热缓存无关 | 好：接收方在自己已热的 buffer 上处理 | Design Guidelines |
| 小消息延迟 | 不一定占优（NIC 处理 + 无 cache 局部性） | 常更优 | Design Guidelines |
| 大块吞吐 | 占优（纯 DMA 搬运） | 受 recv buffer / 处理拖累 | Design Guidelines |
| 可扩展性 / 连接数 | 与 QP 模型耦合（RC 1:1） | 可叠 UD 自建可靠 RPC（FaSST/HERD） | 进阶笔记 |
| 故障 / 语义复杂度 | 远端无 WC，失败处理更难 | recv 失败有明确 WC，语义清晰 | 进阶笔记 |
| 旗舰代表系统 | FaRM（NSDI '15） | FaSST（OSDI '16）、HERD（SIGCOMM '14） | 进阶笔记 |

证据标注：基础笔记 = [[sources/rdma-fundamentals|基础知识（参考笔记）]]；
进阶笔记 = [[sources/rdma-advanced|进阶内容（参考笔记）]]；
Design Guidelines = [[sources/rdma-design-guidelines|Design Guidelines for High Performance RDMA Systems]]。

## 解读

- **决策捷径**：要搬一大块数据、远端不该被打扰 → one-sided；要做 RPC / KV / 事务、消息小、
  或要让远端 CPU 介入 → two-sided。两者经常**在同一系统里混用**（FaRM 用 one-sided 读数据、
  用 two-sided 做控制消息）。
- **「one-sided 更快」是常见误区**。它源于「远端 CPU 零开销」的直觉，但忽略了 NIC 处理
  小消息的开销、缺乏远端 cache 局部性、以及无法复用远端 CPU 已热的数据。Design Guidelines
  的反直觉结论就是：在很多真实负载下 two-sided send/recv 胜出。
- **连接数会改变结论**：当对端数巨大时，RC one-sided 的「N 对端要 N 条 QP」会让 NIC context
  表成为瓶颈；这时用 UD + two-sided 自建可靠 RPC（FaSST/HERD）反而更可扩展。
- **不要在任何一页压平这个分歧**。FaRM 与 FaSST/HERD 是同一时期、同一类问题上的对立设计，
  各有评测支撑；正确表述是「取决于负载和系统目标」。

## 相关页面

- [[concepts/rdma|RDMA]]
- [[sources/rdma-fundamentals|RDMA 基础知识（参考笔记）]]
- [[sources/rdma-advanced|RDMA 进阶内容（参考笔记）]]
- [[sources/rdma-design-guidelines|Design Guidelines for High Performance RDMA Systems]]
- [[syntheses/rdma-reading-guide|RDMA 阅读导图]]
