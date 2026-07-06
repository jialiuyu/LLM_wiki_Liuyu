---
title: ORCA 论文里的 CUDA kernel 是什么意思
type: question
status: active
created: 2026-07-01
updated: 2026-07-01
source_count: 1
tags: [orca, cuda, gpu, kernel, llm-serving]
question: "ORCA 论文里面的 CUDA kernel 是什么意思？这些基本概念应该如何系统学习？有没有什么资料？"
answered: 2026-07-01
---

# ORCA 论文里的 CUDA kernel 是什么意思

## 问题

ORCA 论文里面的 CUDA kernel 是什么意思？这些基本概念应该如何系统学习？有没有什么资料？

## 回答

在 ORCA 论文语境里，`CUDA kernel` 指的是在 GPU 上执行的一段并行程序，通常对应
Transformer execution engine 里的某个 operation 或融合后的 operation。CPU 侧负责发起
`kernel launch`，GPU 上大量 CUDA threads 同时执行这个 kernel。

这不是数学里的“核函数”，也不是操作系统 kernel。更贴近的理解是：

```text
request -> scheduler -> batch/iteration -> execution engine
        -> Transformer operation -> CUDA kernel
```

ORCA 的系统贡献主要在 `iteration-level scheduling` 和 `selective batching`。Scheduler
决定每轮哪些请求进入 batch；execution engine 把这轮 batch 转成 Transformer operation；
底层实际计算由 CUDA ecosystem 中的 kernel、NCCL communication 和相关 GPU 执行机制完成。
证据：[[sources/orca-paper|ORCA 论文]]

## 放回 ORCA 的具体含义

ORCA 的 selective batching 会区分不同 operation 是否适合合批：

- `Linear`、`LayerNorm`、`Add`、`GeLU` 等不依赖请求边界的 operation，可以把所有 token
  展平成 `[sumL,H]` 后统一执行。
- `Attention` 必须保留请求边界，避免不同请求的 token 相互 attention，因此进入
  Attention 前要 Split，按请求分别处理，再 Merge 回后续 token-wise batching。

这解释了为什么论文会谈到 kernel fusion。ORCA 为 `LayerNorm`、`Attention` 和 `GeLU`
实现 fused kernel；其中 Attention 把 `query-key dot product`、`Softmax` 和
`value weighted average` 融合到单个 CUDA kernel。对于 selective batching 拆开的多个
Attention，ORCA 又把不同请求 kernel 的 thread blocks 合并到一次 kernel launch 中，以提高
GPU utilization 并减少 `kernel launch overhead`。证据：[[sources/orca-paper|ORCA 论文]]

## 要先掌握的基本概念

- **Host / device**：CPU 侧通常叫 host，GPU 侧叫 device。Host 组织数据、调度执行，
  device 执行并行计算。
- **Kernel launch**：CPU 侧发起一次 GPU kernel 执行。Launch 本身有开销，所以 ORCA 会关注
  减少 launch 次数。
- **Grid / block / thread**：一个 kernel launch 会创建很多 thread；thread 按 block 分组，
  block 再组成 grid。
- **Memory hierarchy**：GPU 代码的性能常常受 memory access 影响，需要区分 global memory、
  shared memory、register、cache 等层次。
- **Operator / kernel / library**：论文里的 `Linear`、`LayerNorm`、`Attention` 是模型
  operation；CUDA kernel 是某个 operation 的 GPU 实现；cuBLAS、CUTLASS、NCCL 等是常用
  GPU 库或通信库。
- **Fused kernel**：把多个小 operation 合到一个 kernel 里，通常是为了减少中间数据读写、
  减少 launch overhead，或者让数据在更靠近计算单元的位置复用。

## 学习路线

1. 先学 CUDA execution model：`host/device`、`kernel launch`、`grid/block/thread`、
   GPU memory。用 vector add 这类小例子把 `<<<blocks, threads>>>` 和 thread index 跑通。
   官方资料：[CUDA C++ Programming Guide](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/intro-to-cuda-cpp.html)。
2. 再学性能直觉：memory coalescing、occupancy、launch overhead、synchronization、
   profiling。官方资料：[CUDA C++ Best Practices Guide](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html)。
3. 然后学矩阵乘法和深度学习常用算子：GEMM、batched GEMM、mixed precision、cuBLASLt、
   CUTLASS。官方资料：[cuBLAS documentation](https://docs.nvidia.com/cuda/cublas/)；
   [NVIDIA cuBLAS overview](https://developer.nvidia.com/cublas)。
4. 最后回到 LLM serving：读 ORCA 的 selective batching、vLLM 的 PagedAttention，以及
   FlashAttention/FlashInfer 这类 optimized attention kernel。目标不是一开始就手写所有
   kernel，而是能看懂系统什么时候调用库 kernel，什么时候需要自定义 fused kernel。

## 阅读 ORCA 时的定位

读 ORCA 时可以按三层看：

1. **Scheduling 层**：`iteration-level scheduling` 决定请求进入和退出 batch 的时机。
2. **Operation batching 层**：`selective batching` 决定哪些 operation 合批、哪些保留请求边界。
3. **GPU execution 层**：CUDA kernel、fused kernel、NCCL communication 负责实际执行和跨 GPU
   数据移动。

这样读可以避免把 CUDA kernel 误解成 ORCA 的调度算法本身。Kernel 是底层执行单元；ORCA 的论文贡献
是围绕 LLM serving workload 重新组织调度、batching 和分布式执行边界。

## 证据

- [[sources/orca-paper|ORCA 论文]]
- [[entities/orca|ORCA]]
- [[concepts/llm-serving|LLM serving]]
- 官方背景资料：[CUDA C++ Programming Guide](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/intro-to-cuda-cpp.html)
- 官方背景资料：[CUDA C++ Best Practices Guide](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html)
- 官方背景资料：[cuBLAS documentation](https://docs.nvidia.com/cuda/cublas/)

## 证据边界

- ORCA 相关的 selective batching、fused kernel 和实现细节来自 [[sources/orca-paper|ORCA 论文]]。
- CUDA execution model 和学习资料来自 NVIDIA 官方文档背景知识；当前 wiki 还没有独立的 CUDA
  source page 或 concept page。

## 后续问题

- 是否需要把 CUDA 官方文档摄取为 `wiki/sources/` 页面，并沉淀 `CUDA kernel` 独立概念页？
- 学 LLM serving kernel 时，应该先读 cuBLAS/CUTLASS，还是先读 FlashAttention 论文和代码？

## 相关页面

- [[entities/orca|ORCA]]
- [[sources/orca-paper|ORCA 论文]]
- [[concepts/llm-serving|LLM serving]]
- [[concepts/kv-cache|KV cache]]
- [[concepts/pagedattention|PagedAttention]]
