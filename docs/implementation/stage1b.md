# Stage 1 核心引擎 MVP - B: 生命与子弹逻辑

## 约束
- 任何单个代码文件 **不得超过 200 行**，需要拆分时必须拆分。
- 只按本文件指示实现，默认你**不懂架构**、只会按步骤写代码。
- 遇到不确定规则先写入 `docs/` 提问记录，不要自作主张。
- 每完成本文件任务，必须在 `docs/implementation/summarys/` 写执行情况。

## Instructions
按顺序完成以下步骤：
1. 实现 `backend/engine/hp.py`：HP 结构、扣血、死亡判定
2. 实现 `backend/engine/bullet.py`：弹药上限与每 2 秒恢复逻辑
3. 定义射击命中判定的接口（输入玩家/方向/地图）
4. 保证逻辑可通过纯函数调用完成（无全局状态）
5. 把常量集中到 `backend/engine/constants.py`

## Checklist
- [ ] 实现 `backend/engine/hp.py`：HP 结构、扣血、死亡判定
- [ ] 实现 `backend/engine/bullet.py`：弹药上限与每 2 秒恢复逻辑
- [ ] 定义射击命中判定的接口（输入玩家/方向/地图）
- [ ] 保证逻辑可通过纯函数调用完成（无全局状态）
- [ ] 把常量集中到 `backend/engine/constants.py`

## 完成后必须做
- 在 `docs/implementation/summarys/` 新建 `stage1b_summary.md`，写清楚本步骤做了什么、遇到什么问题、未完成项。
- 执行 `git add .` 并 `git push`（统一提交，别只推单个文件）。

