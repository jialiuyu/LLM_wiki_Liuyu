---
title: C++ memory ordering
type: concept
status: active
created: 2026-06-27
updated: 2026-06-27
source_count: 1
tags: [cpp, atomics, memory-order, concurrency]
---

# C++ Memory Ordering

## 摘要

C++ memory ordering 是 C++11 之后并发语义的一组规则，用 `std::atomic`、
`std::memory_order`、mutex 和 fence 来描述哪些跨线程访问可以同步、哪些写入对其他
线程可见，以及 data race 何时导致 undefined behavior。

直觉上，`memory_order_release` 用来发布本线程先前写入，`memory_order_acquire`
用来观察这个发布并禁止后续读写越过它；`memory_order_seq_cst` 在此基础上让相关
atomic 操作参加一条更强的全局顺序。当前页面主要来自
[[sources/cpp-memory-models-programmers|C/C++ 程序员的内存模型]]。

## 关键点

- C++11 把 multi-threaded execution 写进语言语义。两个线程中的 conflicting actions
  如果至少一个不是 atomic，且两者之间没有 `happens-before`，就是 data race，并导致
  undefined behavior。证据：[[sources/cpp-memory-models-programmers|C/C++ 程序员的内存模型]]
- `sequenced-before` 描述单线程内 evaluation 的顺序，但它本身不能保证跨线程可见性。
  编译器仍可在 as-if rule 下做不改变可观察行为的重排序。
- 跨线程的 `happens-before` 需要通过同步建立。论文列出的主要组合包括
  `memory_order_seq_cst`/`memory_order_seq_cst`、`memory_order_release`/
  `memory_order_acquire`、`memory_order_release`/`memory_order_consume`。
- 发布-获取模式可以这样理解：线程 A 先写普通数据，再对 flag 做 release store；
  线程 B 如果用 acquire load 读到这个 flag 值，就能看到 A 在 release 之前的写入。
  证据：[[sources/cpp-memory-models-programmers|C/C++ 程序员的内存模型]]
- `memory_order_relaxed` 仍保证单个 atomic object 的原子修改顺序，但不能建立
  `happens-before`。它适合计数、统计等不需要发布其他数据的场景，不能当作同步信号。
- 每个 atomic object 有自己的 modification order；只有 sequentially consistent
  操作额外参与单一全局顺序。
- `atomic_thread_fence` 可以建立同步，但它需要与相关 atomic 操作组合；单独把 fence
  放在代码里并不自动让任意普通读写跨线程可见。

## 证据

- [[sources/cpp-memory-models-programmers|C/C++ 程序员的内存模型]]

## 张力

- 默认 `std::atomic` 操作是 `memory_order_seq_cst`，推理简单但可能更保守；显式使用
  acquire/release 或 relaxed 可以表达更弱约束，但也更容易写错。
- `memory_order_consume` 在教学上对应 address dependency，但标准和实现层面的可用性
  长期有争议。本页面只记录来源中的 2018 年状态。
- CAS 的 success/failure ordering、release sequence 和 fence 同步规则容易在文字上
  被简化；写底层并发代码时应回到标准草案、编译器文档和 litmus test 验证。

## 开放问题

- 当前 C++23/C++26 working draft 对 `memory_order_consume`、fence 和 data race 的
  文字是否有影响实践的变化？
- LLVM、GCC 和 MSVC 分别如何把这些 order 映射到 x86、ARM 和 RISC-V 指令？

## 相关页面

- [[concepts/memory-model|内存模型]]
- [[questions/cpp-memory-ordering-relaxed-seqcst|relaxed、release/acquire 和 seq_cst 怎么区分]]
