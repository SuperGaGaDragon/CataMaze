# Railway Deployment Fix - Module Import Issue

## ✅ 问题已修复

### 原始错误
```
ModuleNotFoundError: No module named 'storage'
```

### 根本原因
Python import 语义问题：
- Railway 在 `/app` 目录运行
- 代码使用相对导入 `from storage.db import ...`
- Python 的 `sys.path` 不包含 `/app/backend`
- 导致找不到 `storage` 模块

### 解决方案
**所有相对导入改为绝对导入**:

```python
# 修复前 ❌
from storage.db import get_db
from engine.state import WorldState
from api.models import GameRequest
from maps.loader import load_map

# 修复后 ✅
from backend.storage.db import get_db
from backend.engine.state import WorldState
from backend.api.models import GameRequest
from backend.maps.loader import load_map
```

## 📝 修复内容

### 批量替换
```bash
# storage imports
find backend -name "*.py" -exec sed -i 's/from storage\./from backend.storage./g' {} \;

# engine imports
find backend -name "*.py" -exec sed -i 's/from engine\./from backend.engine./g' {} \;

# api imports
find backend -name "*.py" -exec sed -i 's/from api\./from backend.api./g' {} \;

# maps imports
find backend -name "*.py" -exec sed -i 's/from maps\./from backend.maps./g' {} \;
```

### 修复的文件
**API层** (3个文件):
- `backend/api/routes.py`
- `backend/api/game_service.py`
- `backend/api/concurrent_limiter.py`

**Storage层** (5个文件):
- `backend/storage/db.py`
- `backend/storage/models.py`
- `backend/storage/games_store.py`
- `backend/storage/log_store.py`
- `backend/storage/migrate.py`

**Engine层** (4个文件):
- `backend/engine/state_factory.py`
- `backend/engine/observation.py`
- `backend/engine/selfcheck.py`
- `backend/engine/engine.py`

**其他** (2个文件):
- `backend/main.py`
- 所有测试文件 (`test_*.py`)

### 添加的文件
- `backend/personas/__init__.py` - 确保 personas 是 Python 包
- `.gitignore` - 忽略 `__pycache__/` 和 `*.pyc`

## ✅ 本地验证

```bash
$ python3 -c "from backend.api.routes import router; print('✓ Import successful')"
✓ Import successful
```

## 🚀 部署配置（已正确）

### start.sh
```bash
#!/bin/bash
# Initialize database
python -c "from backend.storage.db import init_db; init_db()" || echo "Database initialization failed, continuing..."

# Start FastAPI server
cd /app
uvicorn backend.api.routes:app --host 0.0.0.0 --port ${PORT:-8000}
```

### Procfile
```
web: uvicorn backend.api.routes:app --host 0.0.0.0 --port $PORT
```

### railway.json
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "bash start.sh",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

## 🔍 Railway 部署检查清单

1. **环境变量** (在 Railway 控制台设置):
   - `DATABASE_URL` - Railway 自动提供的 PostgreSQL URL
   - `PORT` - Railway 自动设置

2. **构建日志检查**:
   ```
   ✓ Installing dependencies from requirements.txt
   ✓ Starting with: bash start.sh
   ✓ Database initialization...
   ✓ uvicorn backend.api.routes:app
   ```

3. **运行时日志检查**:
   ```
   INFO:     Started server process
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   INFO:     Uvicorn running on http://0.0.0.0:8000
   ```

## 🎯 测试部署后的 API

### 健康检查
```bash
curl https://your-railway-url/
```

### 创建游戏
```bash
curl -X POST https://your-railway-url/game/new \
  -H "Content-Type: application/json" \
  -d '{"map_name": "default"}'
```

### 查看观察
```bash
curl "https://your-railway-url/game/observe?game_id=YOUR_GAME_ID"
```

## 📊 预期结果

**部署状态**: ✅ Success
**构建时间**: ~2-3 分钟
**API 响应时间**: <100ms

## 🐛 如果仍然失败

### 检查 Railway 日志
```bash
# 在 Railway 控制台查看:
1. Build Logs - 检查依赖安装
2. Deploy Logs - 检查启动过程
3. Runtime Logs - 检查运行时错误
```

### 常见问题

**问题1: 数据库连接失败**
```
解决: 检查 DATABASE_URL 环境变量是否正确
```

**问题2: 端口绑定失败**
```
解决: 确保使用 ${PORT} 环境变量
```

**问题3: 依赖安装失败**
```
解决: 检查 requirements.txt 格式
```

## 📚 相关文档

- [Railway Deployment Guide](https://docs.railway.app/)
- [Python Import System](https://docs.python.org/3/reference/import.html)
- [CataMaze README](README.md)

---

**修复完成**: 2026-01-27
**提交**: 2b37ee1, 49dd532
**状态**: ✅ Ready for Deployment
