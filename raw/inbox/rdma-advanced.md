# RDMA 进阶内容（参考笔记）

> 出处说明：本文是 agent 整理的 RDMA 进阶参考笔记，作为本 wiki 的 raw 来源层引入，
> 配套 `rdma-fundamentals.md`。内容综合下列权威来源，用我自己的话重组；具体协议字段、
> 阈值与硬件能力以原文/当前规范为准：
>
> - InfiniBand Trade Association (IBTA), *InfiniBand Architecture Specification*；
>   *RoCEv2 Specification*（roceinitiative.org）
> - Kalia, Kaminsky, Andersen, *Design Guidelines for High Performance RDMA Systems*
>   (USENIX ATC '16)；同团队 HERD (SIGCOMM '14)、FaSST (OSDI '16)
> - Dragojević et al., *FaRM* (NSDI '15)
> - NVIDIA, *GPUDirect RDMA* 官方文档；*NCCL User Guide*
> - Linux `rdma-core` / perftest / `iproute2` (`rdma`, `rdma-statistic`) 文档
>
> 本文聚焦长期稳定的工程取舍；具体硬件代际（ConnectX-X、HDR/NDR/XDR 速率）以厂商当前
> 文档为准。

## 1. 协议与承载：InfiniBand / RoCE / RoCEv2 / iWARP

RDMA 是一套能力，**承载它的协议栈**有三条主流路线，这是「同一套 verbs API、不同的
underlay」：

- **InfiniBand (IB)**：从链路层开始为 RDMA 从头设计的完整协议栈。链路层用基于信用的
  流控实现**原生无损**，子网由 Subnet Manager（如 OpenSM）集中配置交换机和路径，
  用 LID 寻址。原生低延迟、原生无损、配置开销小，但需要 IB 专用交换机和线缆。
- **RoCE（v1）**：把 IB 的传输层搬到以太网 L2——IB 帧直接封装在以太网帧里，**只能在
  单个 L2 子网内**用，无法路由。实际部署很少。
- **RoCEv2**：把 IB 传输层用 **UDP/IP 封装**（UDP 端口 4791），因此**可跨 L3 路由**，
  能用标准以太网/IP 交换机。代价：以太网默认会丢包，必须额外配无损以太网（见 §2），
  否则性能和稳定性都会塌。这是 RoCEv2 相对 IB 最主要的工程难点。
- **iWARP**：另一套标准，RDMA over TCP（协议层为 MPA + DDP + RDMAP）。能在任意 IP 网络
  上跑、无需无损以太网，但实现和厂商生态比 IB / RoCE 碎片化（主要厂商 Chelsio），
  实际部署少。

三者**对外都暴露同一套 verbs**，应用层代码大体一致；真正的差异在 underlay 的可靠性、
拓扑和运维负担。

## 2. 无损以太网：为什么 RoCEv2 不能「插上网线就用」

以太网默认是「尽力而为、会丢包」的。RDMA 假设下层无损（丢包会导致 go-back-N 重传，
性能断崖式下降）。RoCEv2 必须把以太网配成无损，三件套：

- **PFC（Priority Flow Control，IEEE 802.1Qbb）**：按 802.1p 优先级暂停，而不是全链路
  暂停。把 RoCEv2 流量放到固定优先级（常见 `pfc = 3`），交换机在该优先级 buffer 快满时
  向上游发 pause。**必须端到端、每台交换机和网卡都用同一优先级**，否则断点处仍会丢包。
  代价：head-of-line blocking，pause 风暴扩散的风险。
- **ECN + 拥塞控制（DCQCN / HPCC）**：仅靠 PFC 不够——拥塞会沿路径以 pause 形式扩散，
  造成「拥塞蔓延」。交换机在排队增长时给包打 **ECN 标记（RFC 3168）**，接收端回给发送端
  （CNPs），发送端主动降速（**DCQCN** 是 RoCEv2 上最常用的反应式拥塞控制）。没有拥塞
  控制，PFC 只是把丢包换成了 pause 风暴。
- **DCBX**：在链路上交换能力与配置（PFC 优先级、是否愿意发送/接收 pause 等），让 NIC 和
  交换机协商一致。

工程结论：**「把 RoCE 当普通以太网」是最常见的坑**。IB 是「插上就无损」；RoCEv2 是
「必须显式配 PFC + ECN + 拥塞控制才算无损」。配错时的典型症状是吞吐塌掉、延迟飙升、
`ethtool -S` 里看到大量 `rx_discards` 或 pause 帧。

## 3. 连接 vs 数据报：可扩展性的核心权衡

QP 的 service type 决定「一条 QP 能服务几个对端」与「占多少 NIC 状态」，这是 RDMA 系统
扩展性的关键：

- **RC（Reliable Connection）**最常用，但它是 1:1 的——**N 个对端就要 N 条 QP**（双向则
  2N）。每条 QP 在 NIC 上占固定的 on-chip context（接收 buffer、状态机、序号等），NIC
  的 context 表是有上限的。当对端数（或客户端连接数）很大时，**QP 数量本身成为瓶颈**：
  buffer 占满、cache miss 增加、建连开销累积。这正是 Design Guidelines / FaSST / HERD
  要解决的核心问题。
- **UD（Unreliable Datagram）**：一条 QP 可发往任意对端，QP 数与对端数解耦。代价是
  消息受单 MTU 限制、且要在应用层自己保证可靠和顺序。FaSST、HERD 在 UD 之上自建轻量
  可靠 RPC，换取可扩展性。
- **DC（Dynamically Connected）**：mlx5 引入，按 WR 动态建立连接、用完释放，以接近
  UD 的状态占用拿到接近 RC 的可靠语义，HPC 与存储用得越来越多。

直觉：**RC 像「每个朋友一条专线，质量好但线多了铺不过来」；UD/DC 像「共享线路，要自己
保证送达，但能联系无数人」**。

## 4. one-sided vs two-sided：没有「永远更好」（保留张力）

这是 RDMA 系统设计最核心的争论，本 wiki 在多处强调**不要默认「one-sided 更快」**：

- **one-sided（read/write）**优势：远端 CPU 零参与，适合大块数据搬运、远端不希望被打扰
  的场景。
- **但 one-sided 不总是赢**：小消息时，two-sided 让远端 CPU 能在自己已经热缓存的 buffer
  上处理，反而更快；one-sided 还缺乏「远端执行逻辑」的能力（远端 CPU 不感知，无法插队、
  无法做服务端逻辑），故障处理也更难。
- **三条研究线的张力（务必并读，不要在任何一页压平）**：
  - **FaRM（NSDI '15）**：one-sided 派旗舰，用 one-sided read/write 做分布式事务和锁。
  - **FaSST（OSDI '16）/ HERD（SIGCOMM '14）**：主张 two-sided RPC + UD 在真实 KV/事务
    负载下更快、更可扩展。
  - **Design Guidelines（ATC '16）**：给出工程结论——**取决于负载**（消息大小、是否需要
    远端 cache 局部性、是否需要远端逻辑、连接数）。

经验法则（仍是「取决于」）：**大消息、纯搬运、远端不参与 → one-sided 常赢；小消息、
需要远端处理或热缓存、连接数多 → two-sided 常赢**。详见
`comparisons/rdma-one-sided-vs-two-sided`。

## 5. 内存注册进阶：MR cache 与 ODP

MR 注册开销（见基础笔记 §8）是 RDMA 工程的第二大坑，两条主流解法：

- **MR 缓存**：verbs 库或应用维护一个 MR 池，注销时不真正 deregister，而是放回池里下次
  复用，摊薄注册成本。坑：缓存无界增长会**把物理内存 pin 死**（pin 住的页不可换出、不可
  重新注册），最终撞上系统 locked-memory 上限（`ulimit -l`、`memlock`）。
- **按需注册 / On-Demand Paging (ODP)**：MR 的页**按需**由 NIC 触发缺页并建立映射（需要
  内核与 NIC 支持，Mellanox mlx5 支持），不必一次性 pin 全部内存。
  - **Explicit ODP**：对单个 MR 启用。
  - **Implicit ODP**：对整个进程地址空间启用，任意应用内存都可被 verbs 访问。
  - 代价：缺页时引入额外延迟；适合**稀疏访问**或**地址空间大但只摸一小块**的场景
    （如 GPU/大模型场景），不适合每次都全量命中。

反模式：**「每个请求都 register 一次 buffer，用完 deregister」**——注册开销会吃掉
RDMA 带来的全部收益。正确做法是预注册、缓存或开 ODP。

## 6. 性能调优与测量

基准与工具：

- **perftest** 套件：`ib_send_bw` / `ib_send_lat`（two-sided）、`ib_read_bw` /
  `ib_read_lat`、`ib_write_bw` / `ib_write_lat`（one-sided）、`raw_ethernet_bw`。
  是 RDMA 性能基准的事实标准。
- `ibv_devinfo`、`ibstat`、`rdma link` / `rdma resource`（iproute2）：查设备、端口状态、
  link layer、QP/MR 使用情况。
- `rping`、`rdma-client` / `rdma-server`（rdmacm pingpong）、`udaddy`：连通性自测。

常见调优点：

- **inline**：小消息直接「内联」进 Work Queue Element (WQE)，省一次 WQE 的 DMA，降低小
  消息延迟。
- **signaling rate**：不必为每个 WR 都请求 completion，每 N 个才产生一个 CQE，摊薄 CQ
  开销（但出错时回溯更难）。
- **QP 数量与 SRQ**：多对端时控制 QP 总数；用 SRQ 共享接收 buffer。
- **大页 / NUMA 亲和**：MR 用 huge page 减少 TLB miss；CPU、内存、NIC 跨 NUMA 会拖慢
  doorbell 与 DMA。
- **中断 vs 忙轮询 vs adaptive**：低延迟用忙轮询/`SO_BUSYY_POLL` 类机制；吞吐型用
  adaptive interrupt moderation。
- **GPUDirect RDMA**：见 §7。

## 7. 与 GPU / LLM 集群的连接

这是本 wiki 引入 RDMA 的主要落点（见 `concepts/rdma`、`entities/orca`、`concepts/llm-serving`）：

- **GPUDirect RDMA**：RNIC 直接读写 GPU 显存，数据不经过主机 DRAM，省一次 GPU↔host 拷贝。
  需要 `nvidia-peermem`（旧名 `nv_peer_memory`）内核模块，且 NIC 与 GPU 通常要在同一
  PCIe root complex（同 NUMA）才能拿到真正的 P2P 直连；跨 socket / 跨 PCIe switch 会
  退化为主机内存中转，失去主要收益。
- **NCCL over IB/RoCE**：NCCL 是多 GPU 集合通信运行时（allreduce / allgather 等），
  通过 RDMA transport plugin + GPUDirect RDMA 在节点间搬张量。常见调优环境变量：
  `NCCL_IB_DISABLE`（是否禁用 IB）、`NCCL_IB_HCA`（选哪张网卡）、`NCCL_NET`（外部
  transport plugin，含 GPUDirect 支持）、`NCCL_IB_GID_INDEX`（RoCEv2 GID 选择，常踩坑）、
  `NCCL_DEBUG=INFO`（排错首选项）。
- **Rail-optimized 拓扑**：把 GPU i 与 NIC i 绑成一条「rail」，每条 rail 接到独立的
  leaf switch（rail-attached / rail-optimized）。这样 allreduce 在 rail 内是局部、
  跨 rail 的跳数与拥塞最小化，是大规模训练集群降低 allreduce 延迟的标准做法。
- 回到 LLM 场景：跨节点 RDMA 主要服务**张量并行（TP）的跨机 allreduce**与**流水并行（PP）
  的 activation 传输**；KV cache 的跨节点迁移（如 vLLM 分布式 prefill / disaggregated
  prefill）也越来越依赖高带宽 RDMA。

## 8. 排错诊断速查

- **端口不是 `Active`**：检查链路、子网管理器（IB 要有 OpenSM）、RoCE 的交换机端口配置。
- **MR 注册失败**：`memlock` / `ulimit -l` 太小；ODP 未启用却要注册超大区间。
- **RoCEv2 连不通/性能差**：最常见是 **GID index 选错**（`show_gids`、`NCCL_IB_GID_INDEX`）
  和**无损配置缺失/不一致**（PFC 优先级、ECN）。用 `ethtool -S` 看 `rx_discards`、
  pause 帧计数。
- **GPUDirect RDMA 没生效**：`nvidia-peermem` 模块没加载、NIC 与 GPU 跨 NUMA、容器权限
  （PCIe / CUDA / GID）不足 → 静默退回 bounce-buffer（经主机内存中转）。用
  `nvidia-smi`、`ibv_devinfo -v` 和 NCCL `INFO` 日志确认是否走了 P2P。
