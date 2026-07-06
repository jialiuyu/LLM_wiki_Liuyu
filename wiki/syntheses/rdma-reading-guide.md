---
title: RDMA 阅读导图
type: synthesis
status: active
created: 2026-07-03
updated: 2026-07-05
source_count: 4
tags: [rdma, networking, infiniband, roce, study-guide]
---

# RDMA 阅读导图

## 这份导图在回答什么

这是一份面向“想系统学 RDMA”和“在 GPU / LLM 系统里要用到 RDMA”两类读者的分级读物
推荐，不是单篇来源的译稿或综合。配套概念页见 [[concepts/rdma|RDMA]]。

所有链接均为经检索核对的权威原始来源（厂商文档、会议论文、官方教程）。已建来源页：
[[sources/rdma-fundamentals|基础知识（raw 参考笔记）]]（覆盖第 0/1 层的 verbs、对象模型、
连接类型、内存注册）、[[sources/rdma-advanced|进阶内容（raw 参考笔记）]]（覆盖第 2/3 层的
协议承载、无损以太网、连接可扩展性、one/two-sided 取舍、MR cache/ODP）、
[[sources/rdma-design-guidelines|Design Guidelines]]、[[sources/gpudirect-rdma|GPUDirect
RDMA 官方文档]]；其余仍为外部链接。

one-sided / two-sided 的取舍张力见 [[comparisons/rdma-one-sided-vs-two-sided|对比页]]。

## 一句话定位

RDMA = 网卡硬件直接读写远端应用内存，绕过远端 CPU 和内核。学它要先分清三件事：
（1）协议与承载（IB / RoCE / iWARP）；（2）编程接口（verbs / libibverbs /
librdmacm）；（3）操作语义（one-sided vs two-sided）以及它们在真实系统里的取舍。

## 第 0 层：先建立直觉（入门，1–2 小时）

从“DMA 是什么”一路读到“RDMA 跨网络做了同样的事”。

- **RDMAmojo: Introduction to RDMA** — 从 DMA 讲到 RDMA 的最佳起点，语气轻，适合
  建立第一印象。
  https://www.rdmamojo.com/2014/03/31/remote-direct-memory-access-rdma/
- **NVIDIA RDMA Aware Networks Programming User Manual（前几章）** — 厂商权威，从
  “一台主机内存到另一台”讲起，概念定义最稳。
  https://docs.nvidia.com/rdma-aware-networks-programming-user-manual-1-7.pdf
- **Red Hat: Understanding InfiniBand and RDMA** — Linux 软件栈视角（rdma-core、
  `rdma link`、IPoIB 等），补齐“在 Linux 上长什么样”。
  https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/configuring_infiniband_and_rdma-networks/understanding-infiniband-and-rdma_configuring-infiniband-and-rdma-networks

## 第 1 层：动手写 verbs（入门到中级，半天到一天）

目标是能跑通第一个 RDMA 程序，分清数据路径和连接建立。

- **Netdev 0x16 RDMA Tutorial（Roland Dreier & Jason Gunthorpe）** — 清楚地区分
  libibverbs（数据路径：MR/QP/verbs）和 librdmacm（连接建立、IP 寻址）。两位是
  Linux RDMA 栈的核心维护者。
  https://netdevconf.info/0x16/slides/40/RDMA%2520Tutorial.pdf
- **RDMAmojo: libibverbs** — verbs 与库的速查。
  https://www.rdmamojo.com/2012/05/18/libibverbs/
- **动手**：跑 rdma-core 自带的 pingpong / `rdma-client` 例程；或 GitHub 上的
  [RDMA-Playground](https://github.com/mogami95/RDMA-Playground)。
- 中文读者可参考 cuterwrite 的 RDMA 编程系列作过渡，但结论以官方文档为准。

## 第 2 层：理解机制与取舍（进阶）

这是 RDMA 工程化最核心的一层，决定你怎么把 RDMA 用“对”。

- **Design Guidelines for High Performance RDMA Systems**（Kalia, Kaminsky,
  Andersen；USENIX ATC '16）— RDMA 工程化的核心读物。关键结论：one-sided 不总是
  赢，two-sided RPC 经常更好。来源页：[[sources/rdma-design-guidelines|Design Guidelines]]。
  https://www.usenix.org/system/files/conference/atc16/atc16_paper-kalia.pdf
  - 更易读的同名杂志版：[USENIX ;login: Fall 2016](https://www.usenix.org/system/files/login/articles/login_fall16_07_kalia.pdf)
- **FaRM**（Dragojević et al.；NSDI '15）— one-sided RDMA 的旗舰案例（分布式事务、
  分布式锁）。https://pages.cs.wisc.edu/~shivaram/cs744-readings/FaRM-NSDI.pdf
- **FaSST**（Kalia et al.；OSDI '16）— 用 two-sided 不可靠 datagram 做 RPC，与 FaRM
  形成对照。https://www.usenix.org/system/files/conference/osdi16/osdi16-kalia.pdf
- **HERD**（Kalia et al.；SIGCOMM '14）— KV 场景下对 one-sided 的反思。
  https://www.pdl.cmu.edu/PDL-FTP/Storage/herd-sigcomm2014.pdf
- 读法建议：先读 Design Guidelines；再把 FaRM 和 FaSST 成对读，体会 one/two-sided
  的张力。The Morning Paper 对 [FaRM](https://blog.acolyer.org/2015/05/20/farm-fast-remote-memory/)
  和 [FaSST](https://blog.acolyer.org/2016/12/15/fasst-fast-scalable-and-simple-distributed-transactions-with-two-sided-rdma-datagram-rpcs/)
  的摘要可作为导读。

## 第 3 层：协议与硬件（深度参考）

按需查阅，不必通读。

- **InfiniBand Architecture Specification**（IBTA）— 权威但很重，做硬件 / 驱动时
  必查。
- **RoCEv2 规范**（IBTA / roceinitiative.org）— 以太网承载 RDMA 的规范；配合 PFC、
  ECN、DCBX 等无损以太网资料一起读。
  https://www.roceinitiative.org/infiniband-trade-association-releases-updated-specification-for-remote-direct-memory-access-over-converged-ethernet-roce/

## 第 4 层：在 GPU / LLM 系统里用 RDMA（贴合本知识库）

为什么放进这里：本 wiki 已有 [[concepts/llm-serving|LLM serving]]、
[[entities/orca|ORCA]]（用 NCCL 传 GPU intermediate tensor）、
[[concepts/kv-cache|KV cache]]。RDMA 是这些系统跨节点通信的底层。

- **GPUDirect RDMA 官方文档** — RNIC 直接访问 GPU 显存、绕过主机内存；讲清
  `nvidia-peermem`、PCIe P2P 和编程指南。来源页：[[sources/gpudirect-rdma|GPUDirect RDMA 官方文档]]。
  https://docs.nvidia.com/cuda/gpudirect-rdma/
- **NCCL User Guide（Environment Variables）** — `NCCL_IB_*`、GPUDirect RDMA、
  transport plugin 的调优入口。
  https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html
- **GPU-Initiated Networking for NCCL**（arXiv 2511.15076）— 较新，讨论由 GPU kernel
  直接发起网络传输。https://arxiv.org/html/2511.15076v1
- **实践：vLLM 多节点 LLM 部署如何启用 InfiniBand/RoCE** — 真实部署里的 NCCL 环境变量
  与排错。https://discuss.vllm.ai/t/deploying-multi-node-llm-with-infiband-roce/1344

## 推荐学习路径

- **只想“会用”**：第 0 层 → GPUDirect RDMA 概览 → NCCL User Guide 里 IB / GPUDirect
  相关条目。
- **想系统理解**：第 0 层 → 第 1 层（动手 verbs）→ 第 2 层（Design Guidelines +
  FaRM/FaSST）→ 按需第 3 层。
- **做 GPU / LLM 集群**：系统理解路径 + 第 4 层，并与 [[concepts/llm-serving|LLM serving]]
  的并行 / 通信内容交叉读。

## 最容易踩的坑

- **把 RoCE 当普通以太网**：不加 PFC / ECN 的 RoCEv2 不是“插上网线就能 RDMA”，性能和
  稳定性都会塌。这是 RoCE 相对 InfiniBand 最容易出问题的地方。
- **默认 one-sided 更快**：见 Design Guidelines；小消息、需要 cache 局部性时
  two-sided RPC 常胜出。
- **忘记 memory registration**：RDMA 要求内存 pin + 注册成 MR，大量短生命周期 buffer
  会带来注册开销；用 MR cache 或 on-demand paging（ODP）。
- **以为 GPUDirect RDMA 默认开启**：需要驱动 + peermem 模块 + NIC/GPU 同一 PCIe root
  complex 才能拿到 P2P 直连，跨 NUMA 或跨 switch 会退化。

## 读完后应该能回答

- RDMA 相对普通 socket 网络，绕过了什么、换来什么。
- one-sided 和 two-sided 的区别，以及为什么没有“永远更好”的一种。
- IB / RoCE / RoCEv2 的差别，以及 RoCEv2 为什么需要 PFC / ECN。
- GPUDirect RDMA 解决什么，NCCL 怎么用 RDMA 搬 GPU 张量。
- 回到本 wiki：这些如何影响分布式 LLM 训练 / 推理的跨节点通信。

## 相关页面

- [[concepts/rdma|RDMA]]
- [[concepts/llm-serving|LLM serving]]
- [[entities/orca|ORCA]]
- [[concepts/kv-cache|KV cache]]
