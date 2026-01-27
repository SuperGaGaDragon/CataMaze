# Stage 0 需求定稿与脚手架 - B: 目录与占位文件

## 约束
- 任何单个代码文件 **不得超过 200 行**，需要拆分时必须拆分。
- 只按本文件指示实现，默认你**不懂架构**、只会按步骤写代码。
- 遇到不确定规则先写入 `docs/` 提问记录，不要自作主张。
- 每完成本文件任务，必须在 `docs/implementation/summarys/` 写执行情况。

## Instructions
按顺序完成以下步骤：
1. 创建并补全目录结构（backend/engine、backend/api、backend/storage、backend/agents、frontend/terminal、frontend/UI）
2. 在每个目录放置 `__init__.py` 或 `README.md` 作为占位说明
3. 新增 `backend/requirements.txt` 并写入基础依赖占位（如 fastapi/uvicorn/sqlalchemy/psycopg2-binary/alembic）
4. 新增 `backend/main.py` 占位入口（仅启动应用骨架，不写业务）
5. 新增 `docs/architecture.md`，写出模块职责一览

## Checklist
- [ ] 创建并补全目录结构（backend/engine、backend/api、backend/storage、backend/agents、frontend/terminal、frontend/UI）
- [ ] 在每个目录放置 `__init__.py` 或 `README.md` 作为占位说明
- [ ] 新增 `backend/requirements.txt` 并写入基础依赖占位（如 fastapi/uvicorn/sqlalchemy/psycopg2-binary/alembic）
- [ ] 新增 `backend/main.py` 占位入口（仅启动应用骨架，不写业务）
- [ ] 新增 `docs/architecture.md`，写出模块职责一览

## 完成后必须做
- 在 `docs/implementation/summarys/` 新建 `stage0b_summary.md`，写清楚本步骤做了什么、遇到什么问题、未完成项。
- 执行 `git add .` 并 `git push`（统一提交，别只推单个文件）。

