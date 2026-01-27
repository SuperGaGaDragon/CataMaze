# Stage 2 后端 API + 存储 - E: 并发与 watch

## 约束
- 任何单个代码文件 **不得超过 200 行**，需要拆分时必须拆分。
- 只按本文件指示实现，默认你**不懂架构**、只会按步骤写代码。
- 遇到不确定规则先写入 `docs/` 提问记录，不要自作主张。
- 每完成本文件任务，必须在 `docs/implementation/summarys/` 写执行情况。

## Instructions
按顺序完成以下步骤：
1. 实现 `/game/clear_queue`：清空输入队列
2. 实现 `/game/watch`：返回全局地图视图
3. 加入并发上限 50 局的限制
4. 为所有 API 添加基础错误码
5. 写 `docs/api_spec.md` 更新为最终字段

## Checklist
- [ ] 实现 `/game/clear_queue`：清空输入队列
- [ ] 实现 `/game/watch`：返回全局地图视图
- [ ] 加入并发上限 50 局的限制
- [ ] 为所有 API 添加基础错误码
- [ ] 写 `docs/api_spec.md` 更新为最终字段

## 完成后必须做
- 在 `docs/implementation/summarys/` 新建 `stage2e_summary.md`，写清楚本步骤做了什么、遇到什么问题、未完成项。
- 执行 `git add .` 并 `git push`（统一提交，别只推单个文件）。

