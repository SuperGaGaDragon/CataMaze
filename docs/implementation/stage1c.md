# Stage 1 核心引擎 MVP - C: 世界状态结构

## 约束
- 任何单个代码文件 **不得超过 200 行**，需要拆分时必须拆分。
- 只按本文件指示实现，默认你**不懂架构**、只会按步骤写代码。
- 遇到不确定规则先写入 `docs/` 提问记录，不要自作主张。
- 每完成本文件任务，必须在 `docs/implementation/summarys/` 写执行情况。

## Instructions
按顺序完成以下步骤：
1. 实现 `backend/engine/state.py`：WorldState、AgentState、QueueState 数据结构
2. 定义序列化/反序列化方法（dict <-> dataclass）
3. 定义 tick 计数与时间字段
4. 保证可保存到数据库（只用基本类型）
5. 提供一个 `create_new_state()` 生成初始状态

## Checklist
- [ ] 实现 `backend/engine/state.py`：WorldState、AgentState、QueueState 数据结构
- [ ] 定义序列化/反序列化方法（dict <-> dataclass）
- [ ] 定义 tick 计数与时间字段
- [ ] 保证可保存到数据库（只用基本类型）
- [ ] 提供一个 `create_new_state()` 生成初始状态

## 完成后必须做
- 在 `docs/implementation/summarys/` 新建 `stage1c_summary.md`，写清楚本步骤做了什么、遇到什么问题、未完成项。
- 执行 `git add .` 并 `git push`（统一提交，别只推单个文件）。

