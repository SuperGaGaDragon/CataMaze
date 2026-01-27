# Stage 3 Terminal 版本接入 - B: 命令设计

## 约束
- 任何单个代码文件 **不得超过 200 行**，需要拆分时必须拆分。
- 只按本文件指示实现，默认你**不懂架构**、只会按步骤写代码。
- 遇到不确定规则先写入 `docs/` 提问记录，不要自作主张。
- 每完成本文件任务，必须在 `docs/implementation/summarys/` 写执行情况。

## Instructions
按顺序完成以下步骤：
1. 新增命令文件 `frontend/terminal/commands/catamaze.ts`
2. 支持 `catamaze new`、`catamaze action <key>`、`catamaze tick`
3. 将终端输入映射为 API 调用
4. 实现 ESC 清空队列命令（如 `catamaze clear`）
5. 注册命令到 terminal 命令索引

## Checklist
- [ ] 新增命令文件 `frontend/terminal/commands/catamaze.ts`
- [ ] 支持 `catamaze new`、`catamaze action <key>`、`catamaze tick`
- [ ] 将终端输入映射为 API 调用
- [ ] 实现 ESC 清空队列命令（如 `catamaze clear`）
- [ ] 注册命令到 terminal 命令索引

## 完成后必须做
- 在 `docs/implementation/summarys/` 新建 `stage3b_summary.md`，写清楚本步骤做了什么、遇到什么问题、未完成项。
- 执行 `git add .` 并 `git push`（统一提交，别只推单个文件）。

