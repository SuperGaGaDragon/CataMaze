# Stage 2 后端 API + 存储 - B: 数据库与迁移

## 约束
- 任何单个代码文件 **不得超过 200 行**，需要拆分时必须拆分。
- 只按本文件指示实现，默认你**不懂架构**、只会按步骤写代码。
- 遇到不确定规则先写入 `docs/` 提问记录，不要自作主张。
- 数据库必须使用**自动迁移**（不要手工建表）。
- 数据库连接必须读取 `DATABASE_URL`，值如下：\n  `postgresql://postgres:xkwJlPWNpIYfmsjaPQoRkFJtVLdsrcGW@postgres.railway.internal:5432/railway`\n  不要把密码写死在代码里，只能从环境变量读取。
- 每完成本文件任务，必须在 `docs/implementation/summarys/` 写执行情况。

## Instructions
按顺序完成以下步骤：
1. 新增 `backend/storage/db.py`：数据库连接与 session 管理
2. 新增 `backend/storage/models.py`：Game/Log 表结构
3. 新增 `backend/storage/migrate.py`：自动迁移入口
4. 迁移必须是**自动建表**（启动或脚本触发均可，但不能手工建表）
5. 确保读取 `DATABASE_URL` 环境变量（不能硬编码）
6. 提供最小 migration 运行指令说明

## Checklist
- [ ] 新增 `backend/storage/db.py`：数据库连接与 session 管理
- [ ] 新增 `backend/storage/models.py`：Game/Log 表结构
- [ ] 新增 `backend/storage/migrate.py`：自动迁移入口
- [ ] 迁移必须是**自动建表**（启动或脚本触发均可，但不能手工建表）
- [ ] 确保读取 `DATABASE_URL` 环境变量（不能硬编码）
- [ ] 提供最小 migration 运行指令说明

## 完成后必须做
- 在 `docs/implementation/summarys/` 新建 `stage2b_summary.md`，写清楚本步骤做了什么、遇到什么问题、未完成项。
- 执行 `git add .` 并 `git push`（统一提交，别只推单个文件）。
