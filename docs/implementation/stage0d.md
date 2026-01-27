# Stage 0 需求定稿与脚手架 - D: API 草案

## 约束
- 任何单个代码文件 **不得超过 200 行**，需要拆分时必须拆分。
- 只按本文件指示实现，默认你**不懂架构**、只会按步骤写代码。
- 遇到不确定规则先写入 `docs/` 提问记录，不要自作主张。
- 每完成本文件任务，必须在 `docs/implementation/summarys/` 写执行情况。

## Instructions
按顺序完成以下步骤：
1. 新增 `docs/api_spec.md`，写出每个 endpoint 的请求/响应 JSON 示例
2. 明确 `/game/new` 返回内容（game_id、initial obs、队列等）
3. 明确 `/game/action` 仅入队，不推进 tick
4. 明确 `/game/tick` 的结算返回（新的 obs、事件日志）
5. 明确 `/game/watch` 的权限规则（-watch 后缀）

## Checklist
- [ ] 新增 `docs/api_spec.md`，写出每个 endpoint 的请求/响应 JSON 示例
- [ ] 明确 `/game/new` 返回内容（game_id、initial obs、队列等）
- [ ] 明确 `/game/action` 仅入队，不推进 tick
- [ ] 明确 `/game/tick` 的结算返回（新的 obs、事件日志）
- [ ] 明确 `/game/watch` 的权限规则（-watch 后缀）

## 完成后必须做
- 在 `docs/implementation/summarys/` 新建 `stage0d_summary.md`，写清楚本步骤做了什么、遇到什么问题、未完成项。
- 执行 `git add .` 并 `git push`（统一提交，别只推单个文件）。

