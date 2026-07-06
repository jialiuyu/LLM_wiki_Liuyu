# Wiki 索引

这是 wiki 的内容地图。创建、重命名或实质性修改页面时必须同步更新。

## 核心

- [[overview|总览]] - 当前仓库 LLM wiki 模型的综合说明。

## 来源

- [[sources/karpathy-llm-wiki-pattern|Karpathy 的 LLM Wiki 模式]] - 描述持久、
  来源支撑型 LLM wiki 模式的种子来源。
- [[sources/obsidian-web-clipper-reader|Obsidian Web Clipper Reader]] - 说明
  Web Clipper 的 Reader 模式、入口、阅读视图和可配置项。
- [[sources/vllm-docs-home|vLLM 文档首页]] - 概览 vLLM 的 LLM inference 与
  serving 定位、性能能力、API 支持、模型和硬件覆盖。
- [[sources/vllm-pagedattention-blog|vLLM PagedAttention 发布博客]] - 解释
  vLLM 早期如何用 PagedAttention 改善 KV cache 管理和 serving 吞吐。
- [[sources/pagedattention-paper|PagedAttention 论文]] - SOSP 2023 论文，系统化
  说明 PagedAttention、vLLM 架构和评测结论；已附中文全文阅读版和图 1-19。
- [[sources/orca-paper|ORCA 论文]] - OSDI 2022 论文，提出 iteration-level
  scheduling 与 selective batching；已附中文全文阅读版和图表。
- [[sources/cpp-memory-models-programmers|C/C++ 程序员的内存模型]] - 2018 年教学笔记，
  解释语言/硬件内存模型、sequential consistency、x86-TSO、ARM/POWER 和 C++11
  atomics/fences；已附中文全文阅读版和图 1-2。
- [[sources/rdma-fundamentals|RDMA 基础知识（参考笔记）]] - agent 整理的 raw 参考笔记，
  覆盖 DMA→RDMA、verbs/对象模型、连接类型、内存注册与 pin；综合 NVIDIA manual、IBTA spec、
  Netdev tutorial、rdma-core。
- [[sources/rdma-advanced|RDMA 进阶内容（参考笔记）]] - agent 整理的 raw 参考笔记，覆盖
  IB/RoCE/RoCEv2/iWARP、无损以太网（PFC/ECN/DCQCN）、连接可扩展性、one/two-sided 取舍、
  MR cache/ODP、GPUDirect/NCCL 与 rail-optimized 拓扑。
- [[sources/rdma-design-guidelines|Design Guidelines for High Performance RDMA Systems]] -
  USENIX ATC '16 论文，给出 one-sided/two-sided、连接管理与 memory registration 的
  RDMA 工程指南（外部公开来源，未入 raw）。
- [[sources/gpudirect-rdma|GPUDirect RDMA 官方文档]] - NVIDIA 文档，说明 RNIC 绕过主机
  内存直接访问 GPU 显存的机制与 `nvidia-peermem` 设置（外部官方来源，未入 raw）。

## 概念

- [[concepts/llm-wiki|LLM wiki]] - 由 agent 维护的 Markdown 知识库总体模式。
- [[concepts/raw-sources|Raw 来源]] - 不可变来源层和来源脉络规则。
- [[concepts/wiki-schema|Wiki 规范]] - 让 agent 成为纪律化维护者的操作规则。
- [[concepts/index-and-log|索引和日志]] - 随 wiki 增长而保持可用的导航和时间线文件。
- [[concepts/source-backed-answering|来源支撑的回答]] - 从 wiki 出发并保留引用的问答流程。
- [[concepts/llm-serving|LLM serving]] - 把大语言模型作为高吞吐、可调用服务运行的工程层。
- [[concepts/pagedattention|PagedAttention]] - vLLM 提出的分页式 KV cache 管理方法。
- [[concepts/kv-cache|KV cache]] - LLM autoregressive generation 中保存 attention
  key/value tensor 的缓存。
- [[concepts/memory-model|内存模型]] - 共享内存并发系统中限定读写可见性、重排序和
  允许执行结果的语义规则。
- [[concepts/cpp-memory-ordering|C++ memory ordering]] - C++11 `std::atomic`、
  `std::memory_order`、fence 与 `happens-before` 的同步规则。
- [[concepts/rdma|RDMA]] - 网卡直接读写远端内存、绕过 CPU 的网络能力；锚定
  one-sided/two-sided、verbs、InfiniBand/RoCE 与 GPUDirect RDMA/NCCL 的连接点。

## 实体

- [[entities/obsidian-web-clipper|Obsidian Web Clipper]] - Obsidian 生态中的网页剪藏工具；
  当前聚焦 Reader 模式。
- [[entities/vllm|vLLM]] - 面向 LLM 推理和服务的开源项目。
- [[entities/orca|ORCA]] - 面向自回归 Transformer 生成模型的分布式 serving
  system，提出 iteration-level scheduling 与 selective batching。

## 综合

- [[syntheses/cpp-memory-models-reading-guide|C/C++ 内存模型阅读导图]] - 重新组织
  C/C++ memory model 论文的学习路径，解释译稿难读的原因，并给出 release/acquire、
  hardware model 与 C++ 标准术语的内化框架。
- [[syntheses/rdma-reading-guide|RDMA 阅读导图]] - RDMA 入门到进阶的分级读物推荐，
  含 verbs 教程、Design Guidelines/FaRM/FaSST 等论文，以及贴合 GPU/LLM 系统的
  GPUDirect RDMA 与 NCCL 资料。

## 对比

- [[comparisons/rdma-one-sided-vs-two-sided|RDMA: one-sided vs two-sided]] - 按场景
  对比 RDMA 两类操作，保留 FaRM 与 FaSST/HERD 的研究张力，给出「取决于负载」的决策。

## 问题

- [[questions/cpp-memory-ordering-relaxed-seqcst|relaxed、release/acquire 和 seq_cst 怎么区分]] -
  解释 `relaxed` 解决的 atomicity 问题、release/acquire 读到旧值时为何不同步，以及
  `seq_cst` 如何用全局顺序排除“两边都没看到”的结果。
- [[questions/cuda-kernel-in-orca|ORCA 论文里的 CUDA kernel 是什么意思]] -
  解释 ORCA 中 CUDA kernel/fused kernel 的执行层含义，并给出 CUDA/GPU 基础学习路线。

## 健康检查报告

暂无健康检查报告。
