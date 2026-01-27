# Stage 6 完善与优化 - A: 观战模式

## 约束
- 任何单个代码文件 **不得超过 200 行**，需要拆分时必须拆分。
- 只按本文件指示实现，默认你**不懂架构**、只会按步骤写代码。
- 遇到不确定规则先写入 `docs/` 提问记录，不要自作主张。
- 每完成本文件任务，必须在 `docs/implementation/summarys/` 写执行情况。

## Instructions
按顺序完成以下步骤：
1. 实现 `game_id-watch` 解析逻辑
2. 返回全局地图视图与所有角色位置
3. 避免对外暴露普通 game 细节
4. 在 API 文档标注仅开发者可用
5. 写 `docs/watch_mode.md`

## Checklist
- [ ] 实现 `game_id-watch` 解析逻辑
- [ ] 返回全局地图视图与所有角色位置
- [ ] 避免对外暴露普通 game 细节
- [ ] 在 API 文档标注仅开发者可用
- [ ] 写 `docs/watch_mode.md`

## 完成后必须做
- 在 `docs/implementation/summarys/` 新建 `stage6a_summary.md`，写清楚本步骤做了什么、遇到什么问题、未完成项。
- 执行 `git add .` 并 `git push`（统一提交，别只推单个文件）。

