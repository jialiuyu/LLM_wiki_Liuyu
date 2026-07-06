---
title: C/C++ 程序员的内存模型
type: source
status: active
created: 2026-06-27
updated: 2026-06-29
source_count: 1
tags: [cpp, concurrency, memory-model, atomics, paper]
source_id: src-20260627-cpp-memory-models-programmers
source_url: https://arxiv.org/abs/1803.04432
source_path: raw/assets/1803.04432v1.pdf
author: Manuel Pöter, Jesper Larsson Träff
published: 2018-03-14
ingested: 2026-06-27
---

# C/C++ 程序员的内存模型

## 摘要

这篇 2018 年笔记解释了并发程序为什么必须有明确的
[[concepts/memory-model|内存模型]]：内存模型规定读操作在一组并发写操作下允许看见
哪些值，也约束编译器、处理器和存储系统可以做哪些重排序。

论文先区分语言内存模型和硬件内存模型，再用 sequential consistency、x86-TSO、
ARM/POWER 等模型说明硬件可见性并不等同于源码顺序。最后转向
[[concepts/cpp-memory-ordering|C++ memory ordering]]，概述 C++11 引入的
multi-threaded execution、data race、`std::atomic`、`std::memory_order` 和
`std::atomic_thread_fence`。

原文路径：[raw/assets/1803.04432v1.pdf](../../raw/assets/1803.04432v1.pdf)

## 中文译稿与图版

- [中文 Markdown 译稿](../../output/pdf/cpp-memory-models-programmers-zh.md)
- [中文 PDF 阅读版](../../output/pdf/cpp-memory-models-programmers-zh.pdf)
- 论文图 1-2 已单独导出到 `output/pdf/cpp-memory-models-figures/`，并按原图号嵌入译稿。

译稿保留正文结构、代码 listing、图注和关键标准术语；参考文献条目未逐条翻译。
这是非官方学习译本，引用论文结论时仍应以英文原文为准。

## 关键观点

- 内存模型不是“缓存细节”，而是并发程序的语义边界：它定义哪些执行结果是允许的，
  也反过来定义编译器、CPU 和内存系统可以怎样重排访问。
- 同一段源码至少要区分四种顺序：source code order、program order、execution
  order 和 perceived order。它们可能因为编译器优化、乱序执行、缓存、interconnect
  和存储子系统而不同。
- Sequential consistency 是最直观的推理模型：所有线程操作可以看成保持每个线程
  内顺序的一条全局交错序列。但论文强调，现代处理器通常不会默认提供完整的
  sequential consistency。
- x86-TSO 通过每个硬件线程的 FIFO store buffer 建模。它比 ARM/POWER 更强，但仍
  允许不同地址上的 write 后 read 表现出非 sequentially consistent 的结果，例如
  Dekker 算法需要 `mfence` 或 `lock` 指令才能恢复预期约束。
- ARM 和 POWER 更弱：本地 read/write 可乱序或推测执行，写入也不保证同时对所有
  线程可见。程序员必须用 barrier 和 dependency 正确建立所需顺序。
- C++11 首次把多线程执行纳入标准语义，并把 data race 定义为 undefined behavior。
  线程间可见性要通过 `happens-before`、`synchronizes-with` 和 atomic/fence 操作建立。
- `memory_order_release` / `memory_order_acquire` 可以建立发布-获取式同步；
  `memory_order_relaxed` 只提供 atomic 修改顺序，不建立 `happens-before`；
  `memory_order_seq_cst` 额外参加一条 sequentially consistent 全局顺序。

## 有用细节

- 论文把语言内存模型定义为编译器从 program 到 code 可做的优化、访问改写和重排序
  边界；把硬件内存模型定义为具体架构允许的执行和可见性重排序边界。
- C++ 部分使用 January 2012 的 C++ working draft 来讲 C++11 语义，因为正式 ISO
  标准不是免费公开文本。
- `std::atomic<T>` 操作默认使用 `memory_order_seq_cst`，但可以显式指定更弱的
  `memory_order`。
- `compare_exchange_weak` 可以 spurious failure；CAS 的 success/failure memory
  order 限制在 C++17 中已有调整。
- `atomic_thread_fence` 本身没有绑定某个 atomic object；release fence 与 acquire
  fence 要通过相关 atomic 操作读到同一修改或 release sequence 才能同步。
- 摄取时曾发现重复副本 `raw/assets/1803.04432v1 (1).pdf`。本次用 SHA-256 确认它与
  `raw/assets/1803.04432v1.pdf` 相同，并保留后者作为 canonical 来源路径。

## 张力

- 这是一篇 2018 年教学笔记，不是 C++ 标准本文。它适合作为系统化入门材料；若要做
  当前标准版本的精确判断，需要再核对最新 working draft 或 WG21 paper。
- 论文对 x86-TSO、ARM 和 POWER 的描述服务于 C/C++ 程序员理解，不等同于覆盖所有
  现代微架构、编译器后端或 ABI 的完整规范。
- `memory_order_consume` 在文中按 C++17 临时弃用背景解释；后续 C++ 标准演进需要
  额外来源确认。

## 相关页面

- [[concepts/memory-model|内存模型]]
- [[concepts/cpp-memory-ordering|C++ memory ordering]]
- [[syntheses/cpp-memory-models-reading-guide|C/C++ 内存模型阅读导图]]
