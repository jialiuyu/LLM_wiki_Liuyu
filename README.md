# LLM Wiki Starter

这是一个本地优先的 LLM wiki 起步仓库，基于 Andrej Karpathy 描述的
LLM wiki 模式：

https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

核心结构刻意保持简单：

- `raw/` 存放不可变的来源材料。
- `wiki/` 存放由 LLM 维护的 Markdown 页面。
- `AGENTS.md` 是 Codex 或其他编码 agent 的操作规范。
- `wiki/index.md` 是内容地图。
- `wiki/log.md` 是只追加的活动日志。
- `scripts/` 存放无需额外依赖的检查和搜索工具。

本仓库不需要向量数据库或托管服务。在个人 wiki 规模下，agent 应先阅读
`wiki/index.md`，搜索 Markdown 文件，再打开相关页面和来源。

## 快速开始

1. 把这个文件夹作为 Obsidian vault 打开，或直接浏览 Markdown 文件。
2. 把新来源放入 `raw/inbox/`。
3. 在仓库根目录向 Codex 提问：

   ```text
   请把 raw/inbox/<file> 摄取进这个 LLM wiki。遵守 AGENTS.md，并用中文维护。
   ```

4. 审阅变更后的 wiki 页面。
5. 运行：

   ```bash
   make check
   ```

6. wiki 更新看起来正确后再提交。

## 仓库地图

```text
.
├── AGENTS.md              # Agent 操作规范
├── Makefile               # 常用本地命令
├── raw/
│   ├── inbox/             # 新来源文件
│   ├── processed/         # 可选的用户管理归档
│   └── assets/            # 图片和下载附件
├── wiki/
│   ├── index.md           # 面向内容的地图
│   ├── log.md             # 按时间追加的日志
│   ├── overview.md        # 当前高层综合
│   ├── sources/           # 每个来源一页
│   ├── concepts/          # 概念页
│   ├── entities/          # 人物、组织、项目、地点
│   ├── syntheses/         # 更大的综合笔记
│   ├── comparisons/       # 对比表和分析
│   ├── questions/         # 已归档的问题回答
│   └── lints/             # 周期性健康检查报告
├── templates/             # 页面模板
├── scripts/               # 本地维护工具
└── docs/                  # 面向人的工作流文档
```

## 常用提示词

```text
请摄取 raw/inbox/article.md。创建或更新所有相关 wiki 页面，更新
wiki/index.md，追加 wiki/log.md，并运行 make check。
```

```text
请先使用 wiki 回答这个问题，只有证据不足时再读 raw 来源：<question>
如果答案可复用，请归档到 wiki/questions/。
```

```text
请做一次健康检查。查找断裂链接、过时陈述、矛盾、孤立页面、缺失来源支撑，
以及值得创建独立页面的概念。在 wiki/lints/ 下创建报告。
```

## 当前种子内容

起步 wiki 包含一个来源页，用来总结上面的 LLM wiki gist；还包含几个定义
操作模型的概念页。随着真实知识领域出现，这些页面应该继续被修订。
