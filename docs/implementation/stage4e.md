# Stage 4 UI 版本接入 - E: API 联调

## 约束
- 任何单个代码文件 **不得超过 200 行**，需要拆分时必须拆分。
- 只按本文件指示实现，默认你**不懂架构**、只会按步骤写代码。
- 遇到不确定规则先写入 `docs/` 提问记录，不要自作主张。
- 每完成本文件任务，必须在 `docs/implementation/summarys/` 写执行情况。

## Instructions
按顺序完成以下步骤：
1. 调用 `/game/new` 初始化
2. 调用 `/game/action` 入队
3. 调用 `/game/tick` 推进
4. 调用 `/game/observe` 刷新视野
5. 处理 API 错误并提示

## Checklist
- [ ] 调用 `/game/new` 初始化
- [ ] 调用 `/game/action` 入队
- [ ] 调用 `/game/tick` 推进
- [ ] 调用 `/game/observe` 刷新视野
- [ ] 处理 API 错误并提示

## 完成后必须做
- 在 `docs/implementation/summarys/` 新建 `stage4e_summary.md`，写清楚本步骤做了什么、遇到什么问题、未完成项。
- 执行 `git add .` 并 `git push`（统一提交，别只推单个文件）。

