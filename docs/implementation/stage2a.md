# Stage 2 后端 API + 存储 - A: 后端框架骨架

## 约束
- 任何单个代码文件 **不得超过 200 行**，需要拆分时必须拆分。
- 只按本文件指示实现，默认你**不懂架构**、只会按步骤写代码。
- 遇到不确定规则先写入 `docs/` 提问记录，不要自作主张。
- 每完成本文件任务，必须在 `docs/implementation/summarys/` 写执行情况。

## Instructions
按顺序完成以下步骤：
1. 选择 FastAPI 并搭建 `backend/main.py` 应用入口
2. 新增 `backend/api/__init__.py` 与 `backend/api/routes.py`
3. 配置 CORS 与 JSON 返回格式
4. 加入基本健康检查 `/health`
5. 确保启动命令可运行（仅骨架）

## Checklist
- [ ] 选择 FastAPI 并搭建 `backend/main.py` 应用入口
- [ ] 新增 `backend/api/__init__.py` 与 `backend/api/routes.py`
- [ ] 配置 CORS 与 JSON 返回格式
- [ ] 加入基本健康检查 `/health`
- [ ] 确保启动命令可运行（仅骨架）

## 完成后必须做
- 在 `docs/implementation/summarys/` 新建 `stage2a_summary.md`，写清楚本步骤做了什么、遇到什么问题、未完成项。
- 执行 `git add .` 并 `git push`（统一提交，别只推单个文件）。

