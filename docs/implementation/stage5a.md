# Stage 5 RL Agent 框架 - A: Agent 接口

## 约束
- 任何单个代码文件 **不得超过 200 行**，需要拆分时必须拆分。
- 只按本文件指示实现，默认你**不懂架构**、只会按步骤写代码。
- 遇到不确定规则先写入 `docs/` 提问记录，不要自作主张。
- 每完成本文件任务，必须在 `docs/implementation/summarys/` 写执行情况。

## Instructions
按顺序完成以下步骤：
1. 实现 `backend/agents/base.py` 定义 Agent 接口
2. 实现 `backend/agents/human.py` 作为队列代理
3. 实现 `backend/agents/registry.py` 注册与加载
4. 定义 `backend/agents/personas.py` 数据结构
5. 保证接口可被 engine 调用

## Checklist
- [ ] 实现 `backend/agents/base.py` 定义 Agent 接口
- [ ] 实现 `backend/agents/human.py` 作为队列代理
- [ ] 实现 `backend/agents/registry.py` 注册与加载
- [ ] 定义 `backend/agents/personas.py` 数据结构
- [ ] 保证接口可被 engine 调用

## 完成后必须做
- 在 `docs/implementation/summarys/` 新建 `stage5a_summary.md`，写清楚本步骤做了什么、遇到什么问题、未完成项。
- 执行 `git add .` 并 `git push`（统一提交，别只推单个文件）。

