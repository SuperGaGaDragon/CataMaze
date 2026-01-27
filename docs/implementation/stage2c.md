# Stage 2 后端 API + 存储 - C: 存储层封装

## 约束
- 任何单个代码文件 **不得超过 200 行**，需要拆分时必须拆分。
- 只按本文件指示实现，默认你**不懂架构**、只会按步骤写代码。
- 遇到不确定规则先写入 `docs/` 提问记录，不要自作主张。
- 每完成本文件任务，必须在 `docs/implementation/summarys/` 写执行情况。

## Instructions
按顺序完成以下步骤：
1. 实现 `backend/storage/games_store.py`：save/load/list
2. 实现 `backend/storage/log_store.py`：append/read
3. 存储内容使用序列化后的 world state
4. 保证写入失败时抛出可读错误
5. 每个函数保持小于 200 行

## Checklist
- [ ] 实现 `backend/storage/games_store.py`：save/load/list
- [ ] 实现 `backend/storage/log_store.py`：append/read
- [ ] 存储内容使用序列化后的 world state
- [ ] 保证写入失败时抛出可读错误
- [ ] 每个函数保持小于 200 行

## 完成后必须做
- 在 `docs/implementation/summarys/` 新建 `stage2c_summary.md`，写清楚本步骤做了什么、遇到什么问题、未完成项。
- 执行 `git add .` 并 `git push`（统一提交，别只推单个文件）。

