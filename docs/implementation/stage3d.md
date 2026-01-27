# Stage 3 Terminal 版本接入 - D: 输入队列

## 约束
- 任何单个代码文件 **不得超过 200 行**，需要拆分时必须拆分。
- 只按本文件指示实现，默认你**不懂架构**、只会按步骤写代码。
- 遇到不确定规则先写入 `docs/` 提问记录，不要自作主张。
- 每完成本文件任务，必须在 `docs/implementation/summarys/` 写执行情况。

## Instructions
按顺序完成以下步骤：
1. 支持一次输入多 action -> 全部入队
2. 保证每秒 tick 只消耗一个
3. 实现 `catamaze queue` 查看队列
4. 处理非法输入提示
5. 保证命令文件 <200 行（必要时拆分）

## Checklist
- [ ] 支持一次输入多 action -> 全部入队
- [ ] 保证每秒 tick 只消耗一个
- [ ] 实现 `catamaze queue` 查看队列
- [ ] 处理非法输入提示
- [ ] 保证命令文件 <200 行（必要时拆分）

## 完成后必须做
- 在 `docs/implementation/summarys/` 新建 `stage3d_summary.md`，写清楚本步骤做了什么、遇到什么问题、未完成项。
- 执行 `git add .` 并 `git push`（统一提交，别只推单个文件）。

