---
title: 内存模型
type: concept
status: active
created: 2026-06-27
updated: 2026-06-27
source_count: 1
tags: [concurrency, memory-model, shared-memory]
---

# 内存模型

## 摘要

内存模型是共享内存并发系统的语义规则：它规定在一组并发读写操作中，读操作允许返回
哪些写入结果，并约束编译器、处理器和存储系统可以做哪些重排序。没有明确内存模型，
就很难判断一个并发算法、语言实现或硬件行为是否正确。

当前页面主要来自 [[sources/cpp-memory-models-programmers|C/C++ 程序员的内存模型]]。

## 关键点

- 内存模型的核心问题是“可见性”和“允许结果”，而不是单纯的指令执行先后。
  证据：[[sources/cpp-memory-models-programmers|C/C++ 程序员的内存模型]]
- 语言内存模型约束编译器优化、内存访问改写和重排序；硬件内存模型约束具体处理器
  和存储系统可做的乱序、缓存与传播行为。证据：
  [[sources/cpp-memory-models-programmers|C/C++ 程序员的内存模型]]
- 同一段程序可以涉及 source code order、program order、execution order 和
  perceived order。并发错误常常来自把其中一种顺序误认为另一种顺序。
- Sequential consistency 是最容易推理的模型：所有线程操作可以看成一条保持各线程
  内顺序的全局交错序列。但它通常代价较高，现代硬件默认模型往往更弱。
- x86-TSO 相对强，但 store buffer 仍会让写入先对本线程可见、稍后才传播到共享内存；
  `mfence` 和 `lock` 指令可用于恢复更强顺序。
- ARM 和 POWER 的模型更弱，允许更多本地乱序、推测执行和 write non-atomicity；
  程序员需要用 barrier 和 dependency 明确建立顺序。

## 证据

- [[sources/cpp-memory-models-programmers|C/C++ 程序员的内存模型]]

## 张力

- 弱内存模型提升硬件实现空间、性能和能效，但把正确性负担转移给语言、编译器和
  程序员。
- 纸面上的“程序顺序”不是跨线程可见性的充分证据；必须问这个顺序是否被语言模型、
  原子操作、fence 或硬件 barrier 保护。

## 开放问题

- C++ 标准内存模型如何映射到现代 x86、ARMv8/ARMv9、RISC-V 和 GPU memory model？
- 在无锁数据结构中，哪些约束必须由语言级 atomic 提供，哪些可以依赖平台专有 intrinsic？

## 相关页面

- [[concepts/cpp-memory-ordering|C++ memory ordering]]
