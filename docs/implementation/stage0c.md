# Stage 0 需求定稿与脚手架 - C: 数据结构草案

## 约束
- 任何单个代码文件 **不得超过 200 行**，需要拆分时必须拆分。
- 只按本文件指示实现，默认你**不懂架构**、只会按步骤写代码。
- 遇到不确定规则先写入 `docs/` 提问记录，不要自作主张。
- 每完成本文件任务，必须在 `docs/implementation/summarys/` 写执行情况。

## Instructions
按顺序完成以下步骤：
1. 新增 `docs/data_models.md`，定义 world state、player state、action、observation 的字段草案
2. 将 action 枚举列出：MOVE_UP/DOWN/LEFT/RIGHT、SHOOT_UP/DOWN/LEFT/RIGHT、WAIT
3. 定义队列结构（list）与 tick 行为的约束
4. 定义 HP/Ammo 的上限与恢复规则（与文档一致）
5. 定义胜负条件（出口/死亡）

## Checklist
- [ ] 新增 `docs/data_models.md`，定义 world state、player state、action、observation 的字段草案
- [ ] 将 action 枚举列出：MOVE_UP/DOWN/LEFT/RIGHT、SHOOT_UP/DOWN/LEFT/RIGHT、WAIT
- [ ] 定义队列结构（list）与 tick 行为的约束
- [ ] 定义 HP/Ammo 的上限与恢复规则（与文档一致）
- [ ] 定义胜负条件（出口/死亡）

## 完成后必须做
- 在 `docs/implementation/summarys/` 新建 `stage0c_summary.md`，写清楚本步骤做了什么、遇到什么问题、未完成项。
- 执行 `git add .` 并 `git push`（统一提交，别只推单个文件）。

