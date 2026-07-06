---
title: Design Guidelines for High Performance RDMA Systems
type: source
status: active
created: 2026-07-03
updated: 2026-07-03
source_count: 1
tags: [rdma, paper, high-performance, networking]
source_id: src-20260703-rdma-design-guidelines
source_url: https://www.usenix.org/system/files/conference/atc16/atc16_paper-kalia.pdf
source_path:
author: Anuj Kalia, Michael Kaminsky, David G. Andersen
published: 2016
ingested: 2026-07-03
---

# Design Guidelines for High Performance RDMA Systems

## 摘要

USENIX ATC 2016 论文（CMU 与 Intel Labs）。作者用 Mellanox Connect-IB NIC 在
InfiniBand 上系统评测 RDMA 设计选择，给出“何时用 one-sided、何时用 two-sided”等
工程指南。核心是反直觉结论：在很多负载下 two-sided send/recv 胜过 one-sided
read/write。

原文：[USENIX ATC '16 PDF](https://www.usenix.org/system/files/conference/atc16/atc16_paper-kalia.pdf)；
更易读的同名杂志版：[USENIX ;login: Fall 2016](https://www.usenix.org/system/files/login/articles/login_fall16_07_kalia.pdf)。

注意：本页为外部公开来源，未放入 `raw/`，作为权威背景资料纳入（与 ORCA 中 CUDA 官方
资料的处理一致）。

## 关键观点

- **one-sided（RDMA read/write）不总是最优**。小消息、需要远端 cache 局部性或需要远端
  参与逻辑时，two-sided（send/recv）常常更好。
- 大消息下 one-sided read 的吞吐优势明显，但要权衡 connection、memory registration
  和 ordering 的开销。
- **连接管理是性能关键**：每条 RDMA connection 占用 NIC 资源（QP、recv buffer），
  连接数过多会耗尽 NIC；用不可靠 datagram（如 FaSST）或连接复用可提升可扩展性。
- **memory registration 有开销**；对大量短生命周期 buffer，需要 MR cache 或
  on-demand paging。
- 评测基于 Mellanox Connect-IB over InfiniBand；具体数字不可直接外推到 RoCEv2、新一代
  NIC 或其他 workload。

## 有用细节

- 作者团队（Kalia / Kaminsky / Andersen）也是 HERD（SIGCOMM '14）和 FaSST（OSDI '16）
  的作者，这条线是 RDMA 系统设计最重要的参考之一。
- 配合 [[concepts/rdma|RDMA]] 阅读导图里的 FaRM（one-sided 派）与 FaSST（two-sided 派）
  成对读，能形成 one-sided / two-sided 取舍的完整图景。

## 张力

- 论文的“two-sided 常更好”结论与 FaRM 派“one-sided 更好”形成张力。这是真实的研究分歧，
  不应在任何一页里静默压平。见 [[concepts/rdma|RDMA]] 的张力章节。
- 评测硬件（Connect-IB）距今较远，绝对数值会过时，但 guideline 的定性方向仍被广泛
  引用。

## 相关页面

- [[concepts/rdma|RDMA]]
- [[syntheses/rdma-reading-guide|RDMA 阅读导图]]
