---
title: RDMA 进阶内容（参考笔记）
type: source
status: active
created: 2026-07-05
updated: 2026-07-05
source_count: 1
tags: [rdma, networking, infiniband, roce, advanced, gpu]
source_id: src-20260705-rdma-advanced
source_url:
source_path: raw/inbox/rdma-advanced.md
author: agent 整理（综合 IBTA spec、Design Guidelines/FaRM/FaSST/HERD、GPUDirect RDMA、NCCL、rdma-core/perftest）
published:
ingested: 2026-07-05
---

# RDMA 进阶内容（参考笔记）

## 摘要

agent 整理的 RDMA 进阶参考笔记，落在本仓库 `raw/inbox/rdma-advanced.md`，配套
[[sources/rdma-fundamentals|基础笔记]]。覆盖：InfiniBand / RoCE / RoCEv2 / iWARP 三条承载
路线、RoCEv2 为什么必须配无损以太网（PFC + ECN + DCQCN + DCBX）、连接 vs 数据报的可扩展性
权衡（RC/UD/DC 与 QP 状态瓶颈）、one-sided vs two-sided 的完整张力、内存注册进阶
（MR cache / ODP）、性能调优与测量（perftest、inline、signaling rate）、排错诊断，以及与
GPU / LLM 集群的连接（GPUDirect RDMA、NCCL、rail-optimized 拓扑）。

这是把 [[concepts/rdma|RDMA]] 里「主要依赖厂商文档、缺少第一手 spec」「one/two-sided
张力」等进阶事实首次落到本地来源层。综合 IBTA spec、Kalia 团队论文（Design Guidelines /
HERD / FaSST）、FaRM、GPUDirect RDMA、NCCL、rdma-core/perftest，用自己的话重组。

## 关键观点

- **同一套 verbs，三种 underlay**：IB（原生无损、专用交换机）、RoCEv2（UDP/IP 封装、
  可路由、必须配无损以太网）、iWARP（TCP 承载、生态碎片化）。应用层代码大体一致，差异在
  可靠性、拓扑和运维负担。
- **RoCEv2 不能「插上网线就用」**：以太网默认会丢包，必须 PFC（按优先级暂停，端到端一致）
  + ECN + 拥塞控制（DCQCN）+ DCBX 配成无损。只配 PFC 不配拥塞控制会造成 pause 风暴扩散。
- **QP 数量本身就是瓶颈**：RC 1:1，N 对端要 N~2N 条 QP，每条占 NIC on-chip context。
  这是 FaSST/HERD 用 UD 自建可靠 RPC 的根本动因；mlx5 DC 用动态建连换取可扩展性。
- **one-sided 不是永远更快**：小消息、需要远端热缓存或远端逻辑时 two-sided 常赢；大块
  纯搬运 one-sided 常赢。FaRM（one-sided 派）与 FaSST/HERD（two-sided 派）形成真实研究
  张力，Design Guidelines 给出「取决于负载」的工程结论。
- **MR 注册开销的两种解法**：MR 缓存（复用，但无界会 pin 死内存）和 ODP 按需缺页注册
  （稀疏访问友好，但缺页有延迟）。反模式是「每个请求都 register/deregister」。
- **GPU/LLM 落点**：GPUDirect RDMA 让 RNIC 直读 GPU 显存（需 peermem + 同 NUMA + 同 PCIe
  root complex）；NCCL 通过 RDMA transport plugin 搬张量；rail-optimized 拓扑降低大规模
  allreduce 延迟。

## 有用细节

- RoCEv2 排错最常见坑：GID index 选错（`NCCL_IB_GID_INDEX`）和无损配置缺失/不一致
  （PFC 优先级、ECN），症状是吞吐塌掉、`ethtool -S` 里 `rx_discards` 激增。
- 性能调优杠杆：inline（小消息内联进 WQE 省 DMA）、signaling rate（每 N 个 WR 才产一个
  CQE）、SRQ（共享接收 buffer）、大页 + NUMA 亲和、忙轮询 vs adaptive interrupt。
- perftest 套件（`ib_send_bw`、`ib_read_bw`、`ib_write_bw`）是 RDMA 性能基准事实标准。
- GPUDirect RDMA 没生效会静默退回 bounce-buffer（经主机内存中转），需 `nvidia-peermem`、
  NIC/GPU 同 NUMA、容器 PCIe/CUDA/GID 权限齐备。

## 张力

- **one-sided vs two-sided 必须保留张力**：FaRM 偏 one-sided，FaSST/HERD 偏 two-sided，
  Design Guidelines 给出「取决于负载」。本文与
  [[comparisons/rdma-one-sided-vs-two-sided|对比页]] 都显式保留这种分歧，不压平。
- 本文是 agent 综合多来源整理，非单一来源剪藏；硬件代际（ConnectX-X、HDR/NDR/XDR 速率）、
  具体协议字段以当前 IBTA spec / 厂商文档为准。
- 厂商文档（NVIDIA/Mellanox）描述自家产品偏向正面，对局限（NUMA 退化、RoCE 配置敏感性）
  描述保守，应配合社区排错经验。

## 相关页面

- [[concepts/rdma|RDMA]]
- [[sources/rdma-fundamentals|RDMA 基础知识（参考笔记）]]
- [[sources/rdma-design-guidelines|Design Guidelines for High Performance RDMA Systems]]
- [[sources/gpudirect-rdma|GPUDirect RDMA 官方文档]]
- [[comparisons/rdma-one-sided-vs-two-sided|RDMA: one-sided vs two-sided]]
- [[syntheses/rdma-reading-guide|RDMA 阅读导图]]
- [[concepts/llm-serving|LLM serving]]
- [[entities/orca|ORCA]]
