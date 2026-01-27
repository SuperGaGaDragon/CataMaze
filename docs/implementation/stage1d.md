# Stage 1 核心引擎 MVP - D: 引擎 tick 执行

## 约束
- 任何单个代码文件 **不得超过 200 行**，需要拆分时必须拆分。
- 只按本文件指示实现，默认你**不懂架构**、只会按步骤写代码。
- 遇到不确定规则先写入 `docs/` 提问记录，不要自作主张。
- 每完成本文件任务，必须在 `docs/implementation/summarys/` 写执行情况。

## Instructions
按顺序完成以下步骤：
1. 实现 `backend/engine/engine.py`：保存世界状态与执行 tick
2. tick 内按规则执行：取队列头 action -> 结算移动/射击/恢复
3. 写入事件日志（如 hit/miss/death/exit）
4. 执行完 tick 后输出新的 obs（5x5 视野）
5. 确保每 tick 只执行一个 action

## Checklist
- [ ] 实现 `backend/engine/engine.py`：保存世界状态与执行 tick
- [ ] tick 内按规则执行：取队列头 action -> 结算移动/射击/恢复
- [ ] 写入事件日志（如 hit/miss/death/exit）
- [ ] 执行完 tick 后输出新的 obs（5x5 视野）
- [ ] 确保每 tick 只执行一个 action

## 完成后必须做
- 在 `docs/implementation/summarys/` 新建 `stage1d_summary.md`，写清楚本步骤做了什么、遇到什么问题、未完成项。
- 执行 `git add .` 并 `git push`（统一提交，别只推单个文件）。

