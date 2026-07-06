# RDMA 基础知识（参考笔记）

> 出处说明：本文是 agent 整理的 RDMA 基础参考笔记，作为本 wiki 的 raw 来源层引入，
> 用于把概念页 `concepts/rdma` 中「尚未通过 raw 摄取」「缺少第一手 spec」的事实陈述
> 落到本地来源。内容综合下列权威来源，用我自己的话重组；具体数值/字段以原文为准：
>
> - NVIDIA / Mellanox, *RDMA Aware Networks Programming User Manual*（Mellanox OFED 文档）
> - InfiniBand Trade Association (IBTA), *InfiniBand Architecture Specification*
> - Roland Dreier & Jason Gunthorpe, *RDMA Tutorial*（Netdev 0x16，Linux RDMA 核心维护者）
> - Linux RDMA 项目 `rdma-core`（libibverbs / librdmacm）文档与 man pages
>
> 本文只写长期稳定的基础机制；硬件代际、绝对延迟/带宽数值请查厂商当前文档。

## 1. 从 DMA 到 RDMA：核心一句话

- **DMA**：让设备（磁盘、网卡、GPU）直接搬运数据到/从内存，CPU 不必逐字节参与。
- **RDMA**（Remote DMA）：把 DMA 推过网络——一台机器的网卡（RNIC）**直接读写另一台
  机器应用进程的内存**。

普通 socket 网络的数据路径要经过：应用 buffer → 内核 → 协议栈（TCP/IP）→ 网卡 →
网线 → 网卡 → 协议栈 → 内核 → 应用 buffer，两端各有 CPU 拷贝、上下文切换和系统调用。
RDMA 绕过的是**远端 CPU 与远端内核协议栈**：发起方的网卡直接操作远端已注册的内存，
远端进程的 CPU 在数据传输时不被占用，端到端延迟可压到微秒级，且基本零 CPU 开销。

直觉模型：把 RDMA 看成「网卡硬件实现了你的 send/recv，并在远端也是网卡硬件在搬数据」，
而不是「双方 CPU 通过内核对话」。

## 2. 软件栈与硬件栈

硬件：

- **Channel Adapter (CA)**：RDMA 网卡的通称。**HCA**（Host Channel Adapter）= 主机用
  RNIC（如 Mellanox ConnectX 系列）；**TCA**（Target CA）历史上指嵌入式目标端，现代
  部署里很少单独提。下文统称 RNIC。
- RNIC 自带执行 RDMA 传输逻辑的硬件（解析 verbs、维护连接状态、做 DMA），这是它能绕过
  远端 CPU 的前提。

软件（Linux）：

- 内核侧：`rdma-core` 内核模块（`ib_core`、`ib_uverbs`、厂商驱动如 `mlx5_core`）负责
  MR 注册、地址解析、中断、与硬件通信。
- 用户侧：`libibverbs`（数据路径）+ `librdmacm`（连接建立）。**数据路径在用户态**，
  这是 kernel bypass 的关键：post 一个工作请求后，数据搬运不进内核。

## 3. 编程接口：verbs / libibverbs / librdmacm

- **verbs** 是 RDMA 编程接口的统称（来自 InfiniBand 规范）。Linux 用户态实现分两块：
  - `libibverbs`：**数据路径**——MR、QP、CQ、`post_send` / `post_recv` / `poll_cq`、
    read/write 等原语。
  - `librdmacm`：**连接建立**——用 IP 地址 + 端口建 RDMA 连接（RDMA CM），把 RDMA 编程
    拉近 socket 模型，解决「IB 原生用 LID/GID 寻址、不容易和 TCP 互通」的问题。
- 这两块分工是新手最容易混的：**verbs 管怎么搬数据，CM 管怎么找到对方、握上手**。

## 4. 核心对象（一张词汇表）

| 对象 | 作用 | 关键字段/注意 |
| --- | --- | --- |
| **PD** (Protection Domain) | 访问控制域，把一组对象圈在一起，防止串用 | 同 PD 内的 MR/QP 才能配合 |
| **MR** (Memory Region) | 已注册、可被 RDMA 访问的连续内存区间 | 注册后拿到 `lkey`（本地访问用）和 `rkey`（远端 one-sided 访问用） |
| **MW** (Memory Window) | 更细粒度的临时远端访问授权 | 配合 bind 操作动态授予/撤销 |
| **QP** (Queue Pair) | 发送队列 + 接收队列，是 verbs 操作的入口 | 每个 QP 有一个 transport service type（见 §5） |
| **CQ** (Completion Queue) | 完成事件队列，工作请求完成后入队 | `poll_cq` 轮询，或用 `comp_channel` 等事件、或 busy-poll |
| **WR** (Work Request) | 投递到 QP 的一次工作请求（send/recv/read/write） | 由 `post_send` / `post_recv` 提交 |
| **WC** (Work Completion) | WR 的完成结果，进 CQ | 含状态、字节数、imm 数据 |
| **AH** (Address Header) | UD 数据报寻址用的地址句柄 | UD 模式需要 |
| **SRQ** (Shared Receive Queue) | 多个 QP 共享一个接收队列 | 省接收 buffer |

记忆要点：**应用把 WR 投到 QP → 网卡异步执行 → 完成进 CQ → 应用 poll CQ 拿 WC**。
这条流水线是所有 RDMA 程序的共同骨架。

## 5. 操作语义：one-sided vs two-sided

- **Two-sided（send/recv）**：双方都参与。发送方 `post_send(SEND)`，接收方必须事先
  `post_recv(RECV)` 指定一块 buffer。语义接近消息传递 / RPC。recv 不是「网卡自动放到
  哪」，而是「放进你预先登记的那块 MR」。可携带 immediate data（4 字节）给对端发完成。
- **One-sided（RDMA read / RDMA write）**：只有发起方参与。发起方 `post_send(READ/WRITE)`，
  凭「远端虚拟地址 + rkey」直接读写远端 MR，**远端 CPU 完全不感知**，远端没有 WC。
  `RDMA WRITE` 还可带 immediate（`WRITE_WITH_IMM`），这时对端会收到一个 WC——属于把
  one-sided 搬运和「通知对端」结合的混合形式。
- **Atomics**（RC 专用）：`CMP_SWAP`（compare-and-swap）、`FETCH_ADD`，硬件保证原子。

直觉：one-sided 像直接伸手机到对方内存；two-sided 像把信塞进对方预先摆好的信箱。

## 6. 连接类型（transport service type）

QP 在创建时绑定一种 service type，决定可靠性模型与「能连几个对端」：

- **RC（Reliable Connection）**：可靠、1:1。一条 QP 对应一个对端，消息按序、保可靠。
  最常用，但「每对对端要一条 QP」带来可扩展性代价（见进阶笔记的连接管理）。
- **UC（Unreliable Connection）**：1:1 但不保证可靠/按序，实际很少用。
- **UD（Unreliable Datagram）**：无连接、一条 QP 可发往任意对端（用 AH 寻址），但消息
  受一个 MTU 限制、不保证可靠也不保按序。适合多播和「需要连大量对端」的 RPC 场景
  （FaSST、HERD 的基础）。
- **DC（Dynamically Connected，mlx5）**：按 WR 动态建连，用更少的 QP 状态服务海量对端，
  HPC / 存储里用得越来越多。

## 7. 一次 send/recv 的数据路径（端到端）

发起方：

1. 应用准备一块已注册 MR 作为发送 buffer，填好数据。
2. `post_send(SEND, wr)` 把 WR 投到 QP 的发送队列（通过 doorbell 通知网卡）。
3. RNIC 从该 MR DMA 读出数据，按 service type 打包发到线路。

接收方：

4. 接收方事先 `post_recv(RECV, wr)` 投了一块 MR 作接收 buffer。
5. RNIC 收到包，直接 DMA 写进那块 MR（不经内核协议栈）。
6. 完成进接收方 CQ，接收方 `poll_cq` 拿到 WC（含收到字节数、imm）。

关键点：**两端 CPU 都没碰数据本身**，CPU 只在「准备 WR / 处理 WC」时参与。这是 RDMA
低延迟、低 CPU 占用的来源。

## 8. 内存注册（Memory Region）与 pin

为什么必须注册：

- RNIC 用 DMA 直接访问内存，被访问的物理页**必须驻留在物理内存**（不能被换出），否则
  DMA 会拿到错误数据 → 所以要 **pin（锁页）**。
- RNIC 还需要在它自己的页表里建立「虚拟地址 → 物理地址」映射，并记录访问权限 → 这一步
  是 **register**。
- 注册成功后返回 `lkey`（本地 verbs 用）和 `rkey`（给远端 one-sided 用）。

代价与工程含义：

- 注册/注销都有开销（pin、建映射、与网卡通信），**大块 MR 的注册可达毫秒级**。
- 这带来一系列工程问题（详见进阶笔记）：MR 缓存复用、按需注册（ODP）、避免「每个请求
  都注册一次」的反模式。

## 9. 关键工程直觉速查

- **不是「用上 RDMA 就一定快」**：注册开销、连接数、缓存局部性都会反噬；选 one/two-sided
  要看负载（见进阶笔记的取舍）。
- **数据路径不进内核，但管理路径进**：建连、MR 注册、QP 修改都涉及内核；瓶颈在数据路径，
  管理路径别频繁调用。
- **轮询 vs 事件**：`poll_cq` 忙等延迟最低但烧 CPU；用事件（`comp_channel`）省 CPU 但
  多一次中断/唤醒延迟。低延迟场景常用忙轮询或 adaptive interrupt moderation。
- **rkey 是凭据不是安全**：拿到远端地址 + rkey 就能读写那块 MR，所以 MR 权限、PD、
  MW 绑定是访问控制的重点。
