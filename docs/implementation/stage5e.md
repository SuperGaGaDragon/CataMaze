# Stage 5 RL Agent 框架 - E: 引擎联动

## 约束
- 任何单个代码文件 **不得超过 200 行**，需要拆分时必须拆分。
- 只按本文件指示实现，默认你**不懂架构**、只会按步骤写代码。
- 遇到不确定规则先写入 `docs/` 提问记录，不要自作主张。
- 每完成本文件任务，必须在 `docs/implementation/summarys/` 写执行情况。

## Instructions
按顺序完成以下步骤：
1. 在 engine 中接入 agent 行为选择
2. 保证 human 也走同一接口
3. tick 时先收集所有 agents action
4. RL/log 与 tick 日志合并
5. 验证三个 agent 可执行动作

## Checklist
- [ ] 在 engine 中接入 agent 行为选择
- [ ] 保证 human 也走同一接口
- [ ] tick 时先收集所有 agents action
- [ ] RL/log 与 tick 日志合并
- [ ] 验证三个 agent 可执行动作

## 完成后必须做
- 在 `docs/implementation/summarys/` 新建 `stage5e_summary.md`，写清楚本步骤做了什么、遇到什么问题、未完成项。
- 执行 `git add .` 并 `git push`（统一提交，别只推单个文件）。

