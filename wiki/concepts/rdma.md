---
title: RDMA
type: concept
status: active
created: 2026-07-03
updated: 2026-07-03
source_count: 2
tags: [rdma, networking, infiniband, roce, high-performance]
---

# RDMA

## 摘要

RDMA（Remote Direct Memory Access）让一台机器的网卡（RNIC）直接读写另一台机器应用
内存，绕过远端 CPU 和操作系统内核协议栈。它是 InfiniBand、RoCE、iWARP 等网络技术的
共同能力，在高性能计算、分布式存储与数据库，以及大规模 GPU / LLM 训练和推理集群的
网络层都很常见。

本页锚定 RDMA 的核心机制以及与现有 LLM serving / GPU 内容的连接点。分级读物见
[[syntheses/rdma-reading-guide|RDMA 阅读导图]]。

当前定义主要来自厂商文档（NVIDIA/Mellanox）与学术综述；
[[sources/rdma-design-guidelines|Design Guidelines]] 与
[[sources/gpudirect-rdma|GPUDirect RDMA 官方文档]] 已建来源页，其余仍为外部参考。
详见“证据”章节。

## 关键点

### 直接内存访问与绕过 CPU

- 普通 socket 网络要经过源端和目的端各自的 CPU 拷贝与内核协议栈；RDMA 让网卡硬件
  直接操作应用注册的内存区域，典型地把端到端延迟压到微秒级，且基本不占远端 CPU。
- 证据：[NVIDIA RDMA Aware Networks Programming User Manual](https://docs.nvidia.com/rdma-aware-networks-programming-user-manual-1-7.pdf)

### 两类操作：one-sided 与 two-sided

- **Two-sided（send/recv）**：通信双方都参与。一方 send，另一方必须 post 一个 recv。
  语义接近消息传递 / RPC。FaSST、HERD 用这类原语。
- **One-sided（RDMA read / RDMA write）**：只有发起方参与，远端 CPU 完全不感知。
  发起方直接读写远端预先注册的内存。FaRM 大量使用 one-sided read。
- 工程直觉常见误区是“one-sided 一定更快”。Design Guidelines 给出更细致的结论：在
  很多负载下 two-sided 反而更好，取决于消息大小、缓存局部性和连接管理。
- 证据：[[sources/rdma-design-guidelines|Design Guidelines for High Performance RDMA Systems（USENIX ATC '16）]]

### verbs、libibverbs、librdmacm

- RDMA 编程接口统称 verbs。Linux 用户态实现主要是 libibverbs（数据路径：MR、QP、
  send/recv、read/write）和 librdmacm（用 IP 地址建立连接，把 RDMA 编程拉近 socket
  模型）。
- 证据：[Netdev 0x16 RDMA Tutorial（Dreier & Gunthorpe）](https://netdevconf.info/0x16/slides/40/RDMA%2520Tutorial.pdf)；
  [RDMAmojo: libibverbs](https://www.rdmamojo.com/2012/05/18/libibverbs/)

### 内存注册（Memory Region）

- 要被 RDMA 访问的内存必须先 pin 住并注册成 Memory Region（MR），拿到 lkey / rkey。
  one-sided 操作的“远端地址 + rkey”就是访问凭据。这带来注册开销、MR 缓存、按需
  注册（on-demand paging / ODP）等工程问题。

### 协议与承载：InfiniBand / RoCE / iWARP

- **InfiniBand**：为 RDMA 从头设计的完整协议栈（link layer + transport），原生低延迟、
  原生无损。
- **RoCE / RoCEv2**：把 InfiniBand 的传输层搬到以太网。RoCEv1 限制在 L2 单子网；
  RoCEv2 用 UDP/IP 封装，可跨 L3 路由。要让以太网达到无损，需要 PFC + ECN 等流控与
  拥塞配置，否则性能和稳定性都会塌掉。
- **iWARP**：另一套基于 TCP 的 RDMA 标准，实际部署比 IB / RoCE 少。
- 证据：[IBTA RoCEv2 规范更新公告](https://www.roceinitiative.org/infiniband-trade-association-releases-updated-specification-for-remote-direct-memory-access-over-converged-ethernet-roce/)

### 与 GPU / LLM 系统的连接

- **GPUDirect RDMA**：RNIC 直接访问 GPU 显存，数据不经过主机 DRAM。需要
  `nvidia-peermem`（旧名 `nv_peer_memory`）内核模块，且 NIC 与 GPU 通常要在同一 PCIe
  root complex 才能拿到真正的 P2P 直连，跨 NUMA 会退化。
- **NCCL over InfiniBand / RoCE**：NCCL 是多 GPU 机器学习的集合通信运行时（allreduce
  等）。它通过 RDMA transport plugin 与 GPUDirect RDMA 在节点间搬运张量；典型调优点
  是 `NCCL_IB_HCA`、`NCCL_NET`、是否启用 GPUDirect RDMA 等环境变量。
- 在本 wiki 的脉络里，RDMA 主要影响分布式 LLM 训练 / 推理的跨节点通信。
  [[entities/orca|ORCA]] 提到 GPU intermediate tensor 用 NCCL 通信。
- 证据：[[sources/gpudirect-rdma|GPUDirect RDMA 官方文档]]；
  [NCCL User Guide（Environment Variables）](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html)；
  [[sources/orca-paper|ORCA 论文]]

## 证据

[[sources/rdma-design-guidelines|Design Guidelines]] 与
[[sources/gpudirect-rdma|GPUDirect RDMA 官方文档]] 已建来源页；其余 RDMA 资源仍以外部
权威文档为准，尚未通过 raw 摄取建立独立来源页。完整分级读物见
[[syntheses/rdma-reading-guide|RDMA 阅读导图]]。

- [[sources/rdma-design-guidelines|Design Guidelines for High Performance RDMA Systems]]
- [[sources/gpudirect-rdma|GPUDirect RDMA 官方文档]]
- [[sources/orca-paper|ORCA 论文]]（NCCL 上下文）
- 外部参考（暂无来源页）：NVIDIA RDMA Aware Networks Programming User Manual、
  NCCL User Guide、Netdev 0x16 RDMA Tutorial、IBTA RoCEv2 规范。

## 张力

- **one-sided 还是 two-sided 更好没有定论**。FaRM 偏向 one-sided read；FaSST、HERD
  主张 two-sided RPC 在真实负载下更好；Design Guidelines 给出“取决于负载”的工程
  结论。保留这种张力，不要默认“one-sided 更快”。
- RDMA 概念页的事实目前主要依赖厂商文档（NVIDIA/Mellanox）和学术综述，缺少第一手
  spec（InfiniBand Architecture Specification、RoCEv2 spec 全文）。引用结论时应注意
  厂商文档会偏向自家产品。

## 开放问题

- 在 LLM 训练集群里，RDMA 拓扑（胖树、rail-optimized）、GPUDirect RDMA 与 NCCL 的
  NUMA / PCIe 亲和如何共同决定 allreduce 性能？
- 推理 serving 场景下，跨节点 RDMA 的价值主要在张量并行（TP）的跨机 allreduce，还是
  流水并行（PP）的 activation 传输？
- 是否需要为 InfiniBand、RoCE、NCCL 各自建立独立概念页（目前合并在本页与阅读导图里）。

## 相关页面

- [[syntheses/rdma-reading-guide|RDMA 阅读导图]]
- [[concepts/llm-serving|LLM serving]]
- [[concepts/kv-cache|KV cache]]
- [[entities/orca|ORCA]]
