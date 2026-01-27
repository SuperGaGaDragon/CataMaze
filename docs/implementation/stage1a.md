# Stage 1 核心引擎 MVP - A: 地图与基础类型

## 约束
- 任何单个代码文件 **不得超过 200 行**，需要拆分时必须拆分。
- 只按本文件指示实现，默认你**不懂架构**、只会按步骤写代码。
- 遇到不确定规则先写入 `docs/` 提问记录，不要自作主张。
- 每完成本文件任务，必须在 `docs/implementation/summarys/` 写执行情况。

## Instructions
按顺序完成以下步骤：
1. 实现 `backend/maps/loader.py`：读取 50x50 map，返回二维数组
2. 实现 `backend/engine/actions.py`：Action 枚举与方向向量
3. 实现 `backend/engine/position.py`：位置移动、越界/墙体检测
4. 实现 `backend/engine/local_map.py`：从全局地图裁剪 5x5
5. 为上述模块写最小可运行示例（不需要测试框架）

## Checklist
- [ ] 实现 `backend/maps/loader.py`：读取 50x50 map，返回二维数组
- [ ] 实现 `backend/engine/actions.py`：Action 枚举与方向向量
- [ ] 实现 `backend/engine/position.py`：位置移动、越界/墙体检测
- [ ] 实现 `backend/engine/local_map.py`：从全局地图裁剪 5x5
- [ ] 为上述模块写最小可运行示例（不需要测试框架）

## 完成后必须做
- 在 `docs/implementation/summarys/` 新建 `stage1a_summary.md`，写清楚本步骤做了什么、遇到什么问题、未完成项。
- 执行 `git add .` 并 `git push`（统一提交，别只推单个文件）。

