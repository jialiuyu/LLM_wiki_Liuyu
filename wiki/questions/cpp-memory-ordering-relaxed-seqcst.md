---
title: relaxed、release/acquire 和 seq_cst 怎么区分
type: question
status: active
created: 2026-06-29
updated: 2026-06-29
source_count: 1
tags: [cpp, atomics, memory-order, relaxed, seq-cst]
---

# relaxed、release/acquire 和 seq_cst 怎么区分

## 摘要

`std::memory_order_relaxed` 解决的是“变量自身必须原子，但不用它同步别的数据”的问题。
它是 atomic operation 的最低 ordering 强度，但不是最低等级的同步，因为它不建立
`happens-before`。

`release/acquire` 解决的是“一个线程发布数据，另一个线程通过同一个 atomic 变量接住发布”的问题。
关键条件是：acquire load 必须读到那个 release store 写出的值。

`seq_cst` 解决的是“多个 atomic 操作之间需要一条所有线程都同意的全局顺序”的问题。它不只是
更强的 release/acquire；它提供了 release/acquire 没有的全局排序约束。

证据：[[sources/cpp-memory-models-programmers|C/C++ 程序员的内存模型]]

## relaxed 解决了什么

`relaxed` 适合只关心 atomic 变量自身不丢更新、不被撕裂、不产生 data race 的场景。

例如请求计数：

```cpp
std::atomic<uint64_t> count{0};

void on_request() {
    count.fetch_add(1, std::memory_order_relaxed);
}
```

这里需要保证的是多个线程同时加 `count` 时，更新不会丢失。我们不需要通过 `count` 推断其他普通
变量的可见性。也就是说，`count` 自己要 atomic，但 `count` 不承担“发布数据”的职责。

如果不写 memory order：

```cpp
count.fetch_add(1);
```

默认是 `memory_order_seq_cst`。这通常仍然正确，但语义更强：它要求这次操作参加所有 `seq_cst`
atomic operation 的全局顺序。对于纯计数来说，这个全局顺序往往不是业务需要，只是额外约束。

因此可以这样记：

- 普通变量：多线程并发读写会 data race。
- Atomic + `relaxed`：变量自身原子，但不发布其他内存写入。
- Atomic + `release/acquire`：变量自身原子，并可作为发布/获取通道。
- Atomic + `seq_cst`：变量自身原子，并参与一条更强的全局顺序。

## relaxed 不适合做 ready flag

下面这个写法有问题：

```cpp
int data = 0;
std::atomic<bool> ready{false};

// Thread A
data = 42;
ready.store(true, std::memory_order_relaxed);

// Thread B
if (ready.load(std::memory_order_relaxed)) {
    // 这里不能可靠推断 data == 42
}
```

`ready` 自己是 atomic，所以不会读到半个 bool，也不会和另一个 atomic write 产生 data race。
但 `relaxed` 不发布 `data = 42`。线程 B 即使看到 `ready == true`，也不能据此推断自己已经看见
线程 A 在 store 之前写的普通变量。

正确的发布/获取模式是：

```cpp
int data = 0;
std::atomic<bool> ready{false};

// Thread A
data = 42;
ready.store(true, std::memory_order_release);

// Thread B
if (ready.load(std::memory_order_acquire)) {
    assert(data == 42);
}
```

这里的含义是：

- `release store` 发布它之前的写入，也就是 `data = 42`。
- `acquire load` 如果读到这个 release store 写出的 `true`，就接住这次发布。
- 接住发布后，线程 B 在 acquire 之后的读取必须能看见线程 A 在 release 之前的写入。

## acquire 不是“自动看见所有 release”

一个常见误解是：只要我用了 acquire load，就能看见别的线程已经 release 的东西。

更准确的规则是：

> acquire load 只有在读到某个 release store 写出的值时，才和那个 release store 建立同步。

看这个例子：

```cpp
std::atomic<bool> x{false};
std::atomic<bool> y{false};

// Thread 1
x.store(true, std::memory_order_release);
bool r1 = y.load(std::memory_order_acquire);

// Thread 2
y.store(true, std::memory_order_release);
bool r2 = x.load(std::memory_order_acquire);
```

`r1 == false && r2 == false` 在 release/acquire 下是允许的。

原因是：

- Thread 1 的 acquire load 读的是 `y`。如果它读到初始值 `false`，它没有读到 Thread 2 的
  `y.store(true, release)`，所以没有接住 Thread 2 的发布。
- Thread 2 的 acquire load 读的是 `x`。如果它读到初始值 `false`，它没有读到 Thread 1 的
  `x.store(true, release)`，所以没有接住 Thread 1 的发布。

两个 load 都读到旧值时，没有任何一个 acquire 成功接住对方的 release。因此 release/acquire
不能排除“两边都没看到对方”的结果。

## seq_cst 为什么能排除两边都没看到

如果改成 `seq_cst`：

```cpp
std::atomic<bool> x{false};
std::atomic<bool> y{false};

// Thread 1
x.store(true, std::memory_order_seq_cst);
bool r1 = y.load(std::memory_order_seq_cst);

// Thread 2
y.store(true, std::memory_order_seq_cst);
bool r2 = x.load(std::memory_order_seq_cst);
```

`r1 == false && r2 == false` 就不能成立。

原因是所有 `seq_cst` atomic operation 必须能排进一条全局顺序，并且保留每个线程内部顺序：

```text
Thread 1: store x=true 早于 load y
Thread 2: store y=true 早于 load x
```

如果 `r1 == false`，说明在这条全局顺序里：

```text
load y 早于 store y=true
```

如果 `r2 == false`，说明：

```text
load x 早于 store x=true
```

把这些关系合起来：

```text
store x=true < load y < store y=true < load x < store x=true
```

这形成了环，无法排成一条全局顺序。因此 `seq_cst` 禁止这个结果。

这个例子的重点是：`seq_cst` 多出来的不是“发布能力”。`release/acquire` 已经能发布。`seq_cst`
多出来的是跨多个 atomic 变量的一致全局顺序。

## 什么时候强烈需要 seq_cst

优先考虑 `seq_cst` 的场景：

- 正确性依赖多个 atomic 变量之间的全局相对顺序。
- 代码会从“我没有看到你的 flag”推断“你必须会看到我的 flag”。
- 实现 Dekker/Peterson 一类互斥推理，或多个 atomic flag 共同表达一个协议状态。
- lock-free 算法还没有证明可以降级到 release/acquire 或 relaxed。

优先考虑 `release/acquire` 的场景：

- 同步通道很明确，例如 `ready` flag、队列节点发布、指针发布。
- 读者只有在读到发布者写出的值之后，才需要看到发布者之前的写入。

优先考虑 `relaxed` 的场景：

- 只需要 atomic 变量自身正确，例如统计计数、独立 ID 分配、近似指标采样。
- 不用这个 atomic 值去判断其他普通数据是否已经可见。

## 相关页面

- [[concepts/cpp-memory-ordering|C++ memory ordering]]
- [[syntheses/cpp-memory-models-reading-guide|C/C++ 内存模型阅读导图]]
- [[sources/cpp-memory-models-programmers|C/C++ 程序员的内存模型]]
