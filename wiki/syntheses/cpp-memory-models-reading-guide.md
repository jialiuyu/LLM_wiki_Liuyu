---
title: C/C++ 内存模型阅读导图
type: synthesis
status: active
created: 2026-06-29
updated: 2026-06-29
source_count: 1
tags: [cpp, memory-model, concurrency, study-guide]
---

# C/C++ 内存模型阅读导图

## 这份译稿为什么难读

[[sources/cpp-memory-models-programmers|C/C++ 程序员的内存模型]] 的中文译稿忠于原文句子，
但原文不是面向初学者的“概念内化教程”，而是一篇把硬件模型、语言模型和 C++ 标准术语串起来的
教学笔记。逐句翻译会保留原文的信息顺序，却不会自动补上读者最需要的中间台阶。

主要问题有四个：

- **论证线太长**：文章从“读操作允许看到什么值”开始，经过 sequential consistency、
  x86-TSO、ARM/POWER，最后才落到 C++11。读者如果不知道每一层在回答什么问题，很容易
  读成一串名词。
- **术语层级混在一起**：source code order、program order、execution order、perceived
  order 是“顺序层次”；`sequenced-before`、`synchronizes-with`、`happens-before` 是
  C++ 标准里的关系；`release`、`acquire`、`seq_cst` 是程序员选择的同步强度。它们不是
  同一类概念。
- **缺少一个贯穿例子**：原文给了 Dekker 和 `x/y` atomic 示例，但没有把它们变成一个持续
  使用的心智模型。读者会记住定义，却不知道什么时候该用哪个定义。
- **逐句翻译保留了英文句法**：例如“`A synchronizes-with B`，因此 `A inter-thread-happens-before B`”
  在标准里准确，但如果不先解释“这表示 A 之前写的东西能被 B 之后读到”，读者很难把它变成知识。

这份导图的目标不是替代译稿，而是先建立一套阅读框架，再回头读译稿和原文。

## 一句话总览

内存模型要回答的不是“CPU 实际按什么顺序跑”，而是两个更有用的问题：

- **一个 read 允许看到哪个 write 的值？**
- **编译器、CPU 和内存系统允许把哪些访问重排，哪些不能重排？**

C++ 的 `std::memory_order` 是程序员和编译器之间的契约：你用 atomic、mutex 或 fence 明确建立同步；
编译器和硬件必须保留这些同步所要求的可见性。

证据：[[sources/cpp-memory-models-programmers|C/C++ 程序员的内存模型]]

## 先从一个发布例子开始

先看一个最常见的需求：线程 A 准备好数据，线程 B 等数据准备好后读取它。

```cpp
int data = 0;
std::atomic<bool> ready = false;

// Thread A
data = 42;
ready.store(true, std::memory_order_release);

// Thread B
if (ready.load(std::memory_order_acquire)) {
    assert(data == 42);
}
```

这里真正要保证的不是 `ready` 这个 bool 自己的值。`ready` 只是信号。真正要保证的是：

- 线程 A 在 `release store` 之前写入的 `data = 42`；
- 在线程 B 的 `acquire load` 读到这个 `true` 后，对线程 B 可见。

也就是说，`release` 负责“发布我之前做过的写入”；`acquire` 负责“如果我看到了这个发布信号，
我后面的读取就必须看见发布者之前的写入”。

这就是 `synchronizes-with` 和 `happens-before` 的直觉版本：

- `ready.store(..., release)` 与读到该值的 `ready.load(..., acquire)` 同步。
- 因为同步成立，线程 A 中 `release` 之前的写入 happens-before 线程 B 中 `acquire` 之后的读取。

如果把 `ready` 改成 `memory_order_relaxed`，`ready` 自己仍然是 atomic，不会被撕裂，也有自己的
modification order；但它不再发布 `data`。线程 B 读到 `ready == true` 时，不能据此推断自己已经
看见 `data = 42`。

这就是“atomicity 不等于 ordering”。

## 三层问题：硬件、语言、程序员

读这篇论文时，应把问题分成三层。

| 层次 | 它关心什么 | 典型问题 |
| --- | --- | --- |
| 硬件内存模型 | CPU、cache、store buffer、interconnect 可以怎样让操作乱序或延迟可见 | 为什么 x86 上 Dekker 也可能失败？为什么 ARM/POWER 需要更多 barrier？ |
| 语言内存模型 | 编译器在保留语言语义的前提下可以怎样优化和重排 | 为什么普通变量的 data race 是 undefined behavior？ |
| 程序员同步契约 | 代码里用什么机制告诉编译器和硬件“这里必须建立可见性” | 应该用 mutex、`release/acquire`、`seq_cst`、`relaxed` 还是 fence？ |

这三层不能混读。硬件上“看起来能工作”不等于 C++ 语言层面合法；C++ 语言层面没有 data race，也不表示
每个 atomic 都建立了你想要的跨线程可见性。

## 四种顺序到底在区分什么

论文前面列出的四种 order，最好理解成“同一段代码在不同层的影子”：

- **Source code order**：你写出来的顺序。
- **Program order**：编译器生成的机器码顺序。
- **Execution order**：某个 CPU 实际执行内存指令的顺序。
- **Perceived order**：某个 CPU 观察到自己和其他 CPU 内存操作发生的顺序。

单线程程序里，你通常可以把这些顺序粗略当成一个顺序。并发程序里，这样想会出错。

一个写操作即使已经在本 CPU 执行，也可能还在 store buffer 里，没有传播到共享内存；另一个 CPU
的 read 因此可能还看不到它。也就是说，“我已经写了”和“别人已经能看见”不是同一件事。

## Sequential consistency 是理想模型，不是现实默认值

Sequential consistency 可以理解成：

> 所有线程的操作被放进一条全局时间线；每个线程自己的顺序不变；每次读都读到这条时间线上最近一次写入。

这个模型很适合人脑推理。比如 Dekker 算法中：

```text
Initially: X = 0, Y = 0

Thread 1:
X = 1
r1 = Y

Thread 2:
Y = 1
r2 = X
```

如果所有操作真的处在一条保持线程内顺序的全局时间线上，就不可能 `r1 == 0 && r2 == 0`。
因为只要两个 store 都在两个 load 之前，至少一个 load 会看到另一个线程的 store。

但硬件为了性能不会默认给你完整 sequential consistency。x86 已经算强，仍然可以因为 store buffer
让两个线程都先读到旧值。ARM/POWER 更弱，还允许更多本地乱序、推测执行和非同时传播。

所以 sequential consistency 适合作为“想象中的正确模型”，但不能当成默认现实。

## x86-TSO 的重点：store buffer

x86-TSO 可以先抓住一个核心：每个硬件线程有自己的 FIFO store buffer。

写入发生后，可能先进本线程的 store buffer。本线程后续读同一地址时，可以从自己的 buffer 里读到
最新写入；但其他线程要等这个写入传播到 shared memory 后才能看到。

这解释了两个现象：

- x86 比 ARM/POWER 强，因为它的乱序空间较小。
- x86 仍然不是完整 sequential consistency，因为不同地址上的 write 后 read 可能表现为重排。

对 Dekker 来说，线程 1 的 `X = 1` 可能还停在自己的 store buffer，线程 2 看不到；线程 2 的
`Y = 1` 也可能停在自己的 store buffer，线程 1 看不到。于是两个 load 都读到 0。

`mfence` 或 `lock` 前缀指令的作用，就是在关键点强制 store buffer 传播或建立更强顺序。

## ARM/POWER 的重点：传播不必同时发生

ARM/POWER 更难，是因为它们不仅允许更多本地乱序，还不保证一次写入会同时被所有线程看到。

可以用一个粗糙模型理解：每个线程像是有自己的 memory view。某个线程的写入会逐步传播到其他线程，
传播顺序不一定一致。于是可能出现：

- 线程 2 已经看到线程 1 的某个写入；
- 线程 3 还没看到；
- 或者它们看到不同地址写入的顺序不一样。

因此，ARM/POWER 程序员需要显式使用 barrier 或 dependency 来表达顺序要求。

这一节的价值不是让你记住每种 barrier 的完整表格，而是让你理解为什么 C++ 不能简单说“按源码顺序就行”：
底层硬件本身就不保证每个 core 以同一种顺序看见所有写入。

## C++ 层：先记住四个关系

C++ memory model 里的术语很多，但可以先抓住四个：

| 术语 | 它回答的问题 | 范围 |
| --- | --- | --- |
| `sequenced-before` | 同一线程里，哪个 evaluation 在语义上先发生？ | 单线程 |
| `modification order` | 同一个 atomic object 的所有修改按什么总顺序排列？ | 单个 atomic object |
| `synchronizes-with` | 哪两个同步操作接上了线？ | 跨线程同步点 |
| `happens-before` | A 的内存效果是否必须对 B 可见？ | 单线程与跨线程的传递闭包 |

最容易误解的是 `sequenced-before`。它只管单线程语义，不自动保证跨线程可见性。你在线程 A 里先写
`data` 再写 `ready`，这只是线程 A 内部的顺序；线程 B 是否能据此看到 `data`，取决于你是否在
`ready` 上建立了同步。

## `memory_order` 的选择规则

先用工程规则记，比背标准定义更有用。

| 选择 | 什么时候用 | 你得到什么 |
| --- | --- | --- |
| `mutex` | 默认选择，尤其是共享状态不只是一个 atomic 变量时 | 最容易推理的互斥和可见性 |
| `memory_order_seq_cst` | 需要 atomic，但还没有明确性能理由放松顺序 | 所有 `seq_cst` 操作进入一条全局顺序，最接近人脑模型 |
| `release/acquire` | 一个线程发布数据，另一个线程观察发布信号后读取数据 | 建立发布者之前写入到观察者之后读取的可见性 |
| `memory_order_relaxed` | 独立计数、统计、ID 分配等，只关心 atomic 本身不撕裂，不用它同步其他数据 | 单个 atomic object 的原子性和 modification order，不建立跨线程可见性 |
| fence | 写 lock-free 底层机制，且明确知道 fence 要和哪个 atomic 操作配合 | 可以建立同步，但不是“放一个 fence 就万事大吉” |
| `memory_order_consume` | 一般不要主动使用 | 标准和实现长期有争议，实践中常按 acquire 处理或避免使用 |

一个简单判断：

- 如果你想保护一组共享状态，用 `mutex`。
- 如果你只需要一个 atomic 变量，并且还没证明 `seq_cst` 太慢，用默认 `seq_cst`。
- 如果你在写“数据准备好”这类发布信号，用 `release/acquire`。
- 如果你只是统计次数，不用这个值去判断其他数据是否可见，可以考虑 `relaxed`。
- 如果你需要自己设计 fence/CAS/release sequence，说明你已经在写 lock-free 基础设施，应回到标准、编译器文档和 litmus test 验证。

## 最容易踩的坑

**坑 1：把 atomicity 当成 synchronization。**

`relaxed` atomic 不是普通变量，它仍然是原子的；但它不发布其他普通写入。用 `relaxed` flag 通知
“数据已准备好”通常是错的。

**坑 2：以为源码顺序就是跨线程顺序。**

`data = 42; ready = true;` 在同一线程内有顺序，但另一个线程看到 `ready` 时是否也看到 `data`，
需要同步关系。

**坑 3：以为 x86 上跑过就说明 C++ 合法。**

C++ 的 data race 是语言级 undefined behavior。编译器可以基于“没有 data race”的假设优化。
硬件现象不能反过来证明 C++ 程序合法。

**坑 4：以为 fence 是魔法墙。**

Fence 必须和某个 atomic 操作配合，形成标准定义的同步关系。孤立 fence 不会自动让任意普通读写
跨线程可见。

**坑 5：直接啃 release sequence、CAS failure ordering。**

这些是高级细节。没先理解发布-获取、happens-before、modification order，直接读它们只会变成术语堆叠。

## 推荐阅读顺序

不要按原文从头硬啃。建议按这个顺序内化：

1. 先理解 `data`/`ready` 发布例子：为什么 `release/acquire` 能让普通数据可见。
2. 再看四种顺序：source code order、program order、execution order、perceived order。
3. 用 sequential consistency 建立“理想世界”模型。
4. 用 Dekker + x86 store buffer 打破理想世界。
5. 用 ARM/POWER 理解为什么弱内存模型需要 barrier/dependency。
6. 回到 C++：data race、`sequenced-before`、`synchronizes-with`、`happens-before`。
7. 最后再读 `release sequence`、CAS success/failure ordering 和 fence。

这样读，论文就不再是一组定义，而是一条线：

> 硬件为了性能会让可见顺序变复杂；语言必须给并发程序一个语义边界；程序员用同步操作把自己需要的顺序说清楚。

## 读完后应该内化成什么

读完这篇材料，不需要马上记住每个标准条款。更重要的是形成以下判断：

- 并发读写的核心不是“谁先执行”，而是“谁能看见谁的写入”。
- 普通变量跨线程共享，如果没有同步，就是 data race，C++ 层面直接 undefined behavior。
- Atomic 解决的是两个不同问题：atomicity 和 ordering。不同 `memory_order` 是在选择排序强度。
- `release/acquire` 是最重要的中间层：它比 `seq_cst` 弱，但足以表达大量“发布数据/消费数据”的模式。
- `relaxed` 不是“更快的同步”，而是“没有同步，只保证这个 atomic object 自身的原子修改”。
- 硬件模型解释为什么需要这些规则；C++ 标准模型决定你的 C++ 程序是否有定义。

## 相关页面

- [[sources/cpp-memory-models-programmers|C/C++ 程序员的内存模型]]
- [[concepts/memory-model|内存模型]]
- [[concepts/cpp-memory-ordering|C++ memory ordering]]
- [[questions/cpp-memory-ordering-relaxed-seqcst|relaxed、release/acquire 和 seq_cst 怎么区分]]
