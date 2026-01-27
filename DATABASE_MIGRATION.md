# Database Migration Guide

## ✅ 自动迁移已启用

### 问题
Railway PostgreSQL 数据库中没有表。

### 解决方案
应用启动时自动创建所有必需的表。

## 🚀 工作原理

### FastAPI 启动事件
```python
# backend/main.py
@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup"""
    # 1. Test database connection
    if test_connection():
        logger.info("✓ Database connection successful")

    # 2. Create all tables
    init_db()
    logger.info("✓ Database tables initialized")
```

### 自动创建的表

#### 1. `games` 表
存储游戏状态

**列**:
- `game_id` (String, Primary Key) - 游戏ID
- `tick` (Integer) - 当前tick数
- `world_state` (JSON) - 完整游戏状态
- `game_over` (Boolean) - 游戏是否结束
- `winner_id` (String, nullable) - 获胜者ID
- `created_at` (DateTime) - 创建时间
- `updated_at` (DateTime) - 更新时间

#### 2. `logs` 表
存储游戏事件日志

**列**:
- `id` (Integer, Primary Key, Auto-increment) - 日志ID
- `game_id` (String, Indexed) - 游戏ID
- `tick` (Integer, Indexed) - 发生tick
- `entity_id` (String) - 实体ID
- `event_type` (String) - 事件类型
- `message` (String) - 事件消息
- `extra_data` (JSON, nullable) - 额外数据
- `created_at` (DateTime) - 创建时间

## 🔍 如何验证迁移成功

### 1. 检查 Railway 部署日志

在 Railway 控制台的 **Deploy Logs** 中查找：

```
INFO:__main__:Starting CataMaze API...
INFO:__main__:✓ Database connection successful
INFO:__main__:✓ Database tables initialized
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 2. 检查 PostgreSQL 数据库

**方法1 - Railway Web Console**:
1. 打开 Railway 控制台
2. 点击 PostgreSQL 服务
3. 选择 **Data** 标签
4. 应该看到 `games` 和 `logs` 表

**方法2 - psql 命令行**:
```bash
# 从 Railway 获取 DATABASE_URL
railway variables

# 连接数据库
psql $DATABASE_URL

# 列出所有表
\dt

# 查看表结构
\d games
\d logs

# 退出
\q
```

**方法3 - Python 脚本**:
```bash
# 本地检查 (需要设置 DATABASE_URL)
export DATABASE_URL="postgresql://user:pass@host:5432/dbname"
python -m backend.check_db
```

### 3. 测试 API 创建游戏

```bash
# 创建游戏（会在数据库中插入记录）
curl -X POST https://your-railway-url/game/new \
  -H "Content-Type: application/json" \
  -d '{"map_name": "default"}'

# 返回示例
{
  "game_id": "abc123",
  "observation": {...}
}
```

然后检查数据库：
```sql
-- 在 psql 中
SELECT game_id, tick, game_over FROM games LIMIT 5;
SELECT game_id, tick, event_type FROM logs LIMIT 10;
```

## 🛠️ 手动迁移（如果需要）

### 本地环境

```bash
# 使用 check_db.py 脚本
python -m backend.check_db init

# 或直接用 Python
python -c "from backend.storage.db import init_db; init_db()"
```

### Railway 环境

**方法1 - 重新部署**:
- 应用会在启动时自动运行迁移
- 不需要手动操作

**方法2 - Railway CLI**:
```bash
# 安装 Railway CLI
npm i -g @railway/cli

# 登录
railway login

# 连接到项目
railway link

# 运行迁移命令
railway run python -m backend.check_db init
```

**方法3 - 添加 Environment Variable**:
在 Railway 控制台设置：
- `RUN_MIGRATION=true`

然后修改 `start.sh`:
```bash
if [ "$RUN_MIGRATION" = "true" ]; then
  python -m backend.check_db init
fi
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

## 🐛 故障排除

### 问题1: 数据库连接失败

**症状**:
```
✗ Database connection failed
Cannot connect to database
```

**解决**:
- 检查 `DATABASE_URL` 环境变量
- 确认 PostgreSQL 服务正在运行
- 检查网络连接

### 问题2: 表已存在错误

**症状**:
```
Table 'games' already exists
```

**解决**:
- 这是正常的！SQLAlchemy 会跳过已存在的表
- 不会覆盖现有数据

### 问题3: 表未创建

**症状**:
```
✓ Database connection successful
✓ Database tables initialized
# 但数据库中仍然没有表
```

**解决**:
1. 确认 models.py 正确导入
2. 检查 Base.metadata 是否包含模型
3. 手动运行迁移脚本

```python
# 调试脚本
from backend.storage.db import Base, engine
from backend.storage.models import Game, Log
from sqlalchemy import inspect

# 查看注册的表
print("Registered tables:", Base.metadata.tables.keys())

# 创建表
Base.metadata.create_all(bind=engine)

# 验证
inspector = inspect(engine)
print("Created tables:", inspector.get_table_names())
```

## 📊 数据库模式图

```
┌─────────────────────┐
│       games         │
├─────────────────────┤
│ game_id (PK)        │
│ tick                │
│ world_state (JSON)  │
│ game_over           │
│ winner_id           │
│ created_at          │
│ updated_at          │
└─────────────────────┘
         │
         │ 1:N
         │
         ▼
┌─────────────────────┐
│        logs         │
├─────────────────────┤
│ id (PK)             │
│ game_id (FK, IDX)   │
│ tick (IDX)          │
│ entity_id           │
│ event_type          │
│ message             │
│ extra_data (JSON)   │
│ created_at          │
└─────────────────────┘
```

## 📝 最佳实践

1. **不要手动修改生产数据库**: 使用迁移脚本
2. **备份数据**: 在运行迁移前备份
3. **测试迁移**: 先在开发环境测试
4. **监控日志**: 检查迁移是否成功

## 🔗 相关文档

- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Railway PostgreSQL Guide](https://docs.railway.app/databases/postgresql)
- [FastAPI Startup Events](https://fastapi.tiangolo.com/advanced/events/)

---

**更新时间**: 2026-01-27
**提交**: 3e6f8b5
**状态**: ✅ Auto-migration Enabled
