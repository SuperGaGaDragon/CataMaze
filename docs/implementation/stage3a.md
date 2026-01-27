# Stage 3 Terminal 版本接入 - A: 接入准备

## 约束
- 任何单个代码文件 **不得超过 200 行**，需要拆分时必须拆分。
- 只按本文件指示实现，默认你**不懂架构**、只会按步骤写代码。
- 遇到不确定规则先写入 `docs/` 提问记录，不要自作主张。
- 每完成本文件任务，必须在 `docs/implementation/summarys/` 写执行情况。

## Instructions
按顺序完成以下步骤：
1. 阅读 `desktop/catachess/patch/modules/terminal/README.md`
2. 确定是用 `TerminalLauncher` 还是 `TerminalWindow`
3. 创建 `frontend/terminal/index.tsx` 作为入口
4. 准备与后端 API 通讯的 client
5. 保证入口文件 <200 行

## Checklist
- [ ] 阅读 `desktop/catachess/patch/modules/terminal/README.md`
- [ ] 确定是用 `TerminalLauncher` 还是 `TerminalWindow`
- [ ] 创建 `frontend/terminal/index.tsx` 作为入口
- [ ] 准备与后端 API 通讯的 client
- [ ] 保证入口文件 <200 行

## 完成后必须做
- 在 `docs/implementation/summarys/` 新建 `stage3a_summary.md`，写清楚本步骤做了什么、遇到什么问题、未完成项。
- 执行 `git add .` 并 `git push`（统一提交，别只推单个文件）。

