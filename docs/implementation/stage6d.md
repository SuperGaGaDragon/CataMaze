# Stage 6 完善与优化 - D: 错误处理

## 约束
- 任何单个代码文件 **不得超过 200 行**，需要拆分时必须拆分。
- 只按本文件指示实现，默认你**不懂架构**、只会按步骤写代码。
- 遇到不确定规则先写入 `docs/` 提问记录，不要自作主张。
- 每完成本文件任务，必须在 `docs/implementation/summarys/` 写执行情况。

## Instructions
按顺序完成以下步骤：
1. 为所有 API 加入统一错误响应结构
2. 处理非法 action/越界/不存在 game_id
3. 处理数据库失败与恢复
4. 前端提示友好错误
5. 写 `docs/errors.md`

## Checklist
- [ ] 为所有 API 加入统一错误响应结构
- [ ] 处理非法 action/越界/不存在 game_id
- [ ] 处理数据库失败与恢复
- [ ] 前端提示友好错误
- [ ] 写 `docs/errors.md`

## 完成后必须做
- 在 `docs/implementation/summarys/` 新建 `stage6d_summary.md`，写清楚本步骤做了什么、遇到什么问题、未完成项。
- 执行 `git add .` 并 `git push`（统一提交，别只推单个文件）。

