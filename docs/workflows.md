# 工作流

这些工作流是 `AGENTS.md` 的面向人版本。

## 摄取来源

1. 把来源放入 `raw/inbox/`。
2. 要求 agent 摄取指定文件。
3. agent 在 `wiki/sources/` 下创建来源页。
4. agent 更新相关 concept、entity、synthesis、comparison 或 question 页面。
5. agent 更新 `wiki/index.md`。
6. agent 追加 `wiki/log.md`。
7. agent 运行 `make check`。
8. 你审阅 diff。

## 提问

要求 agent 优先从 wiki 回答。如果答案形成了长期有用的知识，让 agent 把它
归档到 `wiki/questions/`、`wiki/syntheses/` 或 `wiki/comparisons/`。

## 做健康检查

要求 agent 做一次 lint。若输出包含有价值的发现，应在 `wiki/lints/` 下形成
一页报告。

## 演进规范

当你发现重复出现的维护错误时，更新 `AGENTS.md`。这是让未来 agent 会话更容易
维护这个 wiki 的方式。
