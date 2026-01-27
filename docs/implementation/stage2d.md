# Stage 2 后端 API + 存储 - D: API 端点实现

## 约束
- 任何单个代码文件 **不得超过 200 行**，需要拆分时必须拆分。
- 只按本文件指示实现，默认你**不懂架构**、只会按步骤写代码。
- 遇到不确定规则先写入 `docs/` 提问记录，不要自作主张。
- 每完成本文件任务，必须在 `docs/implementation/summarys/` 写执行情况。

## Instructions
按顺序完成以下步骤：
1. 实现 `/game/new`：创建 state、保存、返回 obs
2. 实现 `/game/action`：仅入队，不 tick
3. 实现 `/game/tick`：调用引擎 tick、保存
4. 实现 `/game/observe`：返回当前 obs
5. 实现 `/game/resume`：按 game_id 取最新状态

## Checklist
- [ ] 实现 `/game/new`：创建 state、保存、返回 obs
- [ ] 实现 `/game/action`：仅入队，不 tick
- [ ] 实现 `/game/tick`：调用引擎 tick、保存
- [ ] 实现 `/game/observe`：返回当前 obs
- [ ] 实现 `/game/resume`：按 game_id 取最新状态

## 完成后必须做
- 在 `docs/implementation/summarys/` 新建 `stage2d_summary.md`，写清楚本步骤做了什么、遇到什么问题、未完成项。
- 执行 `git add .` 并 `git push`（统一提交，别只推单个文件）。

