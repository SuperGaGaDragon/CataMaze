# Stage 1 核心引擎 MVP - E: 引擎自检

## 约束
- 任何单个代码文件 **不得超过 200 行**，需要拆分时必须拆分。
- 只按本文件指示实现，默认你**不懂架构**、只会按步骤写代码。
- 遇到不确定规则先写入 `docs/` 提问记录，不要自作主张。
- 每完成本文件任务，必须在 `docs/implementation/summarys/` 写执行情况。

## Instructions
按顺序完成以下步骤：
1. 写 `backend/engine/selfcheck.py`：构造一局最小流程
2. 验证地图载入、移动、射击、恢复、死亡、出口
3. 输出控制台日志（纯 print）用于人工检查
4. 不依赖数据库或 API
5. 确保所有模块文件 <200 行

## Checklist
- [ ] 写 `backend/engine/selfcheck.py`：构造一局最小流程
- [ ] 验证地图载入、移动、射击、恢复、死亡、出口
- [ ] 输出控制台日志（纯 print）用于人工检查
- [ ] 不依赖数据库或 API
- [ ] 确保所有模块文件 <200 行

## 完成后必须做
- 在 `docs/implementation/summarys/` 新建 `stage1e_summary.md`，写清楚本步骤做了什么、遇到什么问题、未完成项。
- 执行 `git add .` 并 `git push`（统一提交，别只推单个文件）。

