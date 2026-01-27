# Logging System

CataMaze的日志系统说明和最佳实践。

## 日志级别

### DEBUG
**用途**: 详细的调试信息

**示例**:
```python
logger.debug(f"Processing tick {tick} for game {game_id}")
logger.debug(f"Entity {entity_id} position: {position}")
```

### INFO
**用途**: 一般信息记录

**示例**:
```python
logger.info(f"New game created: {game_id}")
logger.info(f"Game {game_id} ended with status: {status}")
```

### WARNING
**用途**: 警告信息，不影响正常运行

**示例**:
```python
logger.warning(f"Game {game_id} approaching tick limit")
logger.warning(f"High memory usage: {memory_usage}MB")
```

### ERROR
**用途**: 错误信息，影响功能但不致命

**示例**:
```python
logger.error(f"Failed to load map {map_name}: {error}")
logger.error(f"Database query failed: {error}")
```

### CRITICAL
**用途**: 严重错误，可能导致系统崩溃

**示例**:
```python
logger.critical(f"Database connection lost")
logger.critical(f"Out of memory")
```

## 日志配置

### 基本配置
```python
import logging

# 配置日志格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('catamaze.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### 高级配置
创建 `logging_config.json`:
```json
{
  "version": 1,
  "disable_existing_loggers": false,
  "formatters": {
    "default": {
      "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    },
    "detailed": {
      "format": "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
    }
  },
  "handlers": {
    "console": {
      "class": "logging.StreamHandler",
      "level": "INFO",
      "formatter": "default",
      "stream": "ext://sys.stdout"
    },
    "file": {
      "class": "logging.handlers.RotatingFileHandler",
      "level": "DEBUG",
      "formatter": "detailed",
      "filename": "logs/catamaze.log",
      "maxBytes": 10485760,
      "backupCount": 5
    }
  },
  "loggers": {
    "backend.engine": {
      "level": "DEBUG",
      "handlers": ["console", "file"],
      "propagate": false
    },
    "backend.api": {
      "level": "INFO",
      "handlers": ["console", "file"],
      "propagate": false
    }
  },
  "root": {
    "level": "INFO",
    "handlers": ["console", "file"]
  }
}
```

使用配置:
```python
import logging.config
import json

with open('logging_config.json', 'r') as f:
    config = json.load(f)
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)
```

## 模块日志

### Engine日志
```python
# backend/engine/game.py
import logging

logger = logging.getLogger(__name__)

class Game:
    def __init__(self, game_id, map_name):
        logger.info(f"Initializing game {game_id} with map {map_name}")

    def tick(self):
        logger.debug(f"Game {self.game_id} tick {self.current_tick}")
        # 游戏逻辑
        logger.debug(f"Entities processed: {len(self.entities)}")
```

### API日志
```python
# backend/api/routes.py
import logging

logger = logging.getLogger(__name__)

@app.post("/game/new")
def create_game(request: GameRequest):
    logger.info(f"Received create_game request: {request.map_name}")

    try:
        game = create_new_game(request.map_name)
        logger.info(f"Game created successfully: {game.game_id}")
        return {"game_id": game.game_id}
    except Exception as e:
        logger.error(f"Failed to create game: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

### Storage日志
```python
# backend/storage/db.py
import logging

logger = logging.getLogger(__name__)

class GameStorage:
    def save_game(self, game_state):
        logger.debug(f"Saving game {game_state.game_id}")
        try:
            # 保存逻辑
            logger.debug("Game saved successfully")
        except Exception as e:
            logger.error(f"Failed to save game: {e}")
            raise
```

## 事件日志

### 游戏事件
```python
# 记录重要游戏事件
logger.info(f"Player hit enemy at ({x}, {y})")
logger.info(f"Enemy killed by player")
logger.info(f"Player picked up health pack")
logger.warning(f"Player HP critical: {hp}/5")
```

### API请求日志
```python
# 记录所有API请求
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response
```

### 性能日志
```python
import time

def log_performance(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start_time
        logger.debug(f"{func.__name__} took {elapsed:.3f}s")
        return result
    return wrapper

@log_performance
def process_tick(game_id):
    # 处理逻辑
    pass
```

## 日志分析

### 查看最近错误
```bash
# 查看最近的错误日志
tail -f logs/catamaze.log | grep ERROR

# 统计错误数量
grep ERROR logs/catamaze.log | wc -l
```

### 性能分析
```bash
# 查找慢查询
grep "took" logs/catamaze.log | awk '{if ($NF > 1.0) print}'

# 统计API调用频率
grep "Request:" logs/catamaze.log | awk '{print $5}' | sort | uniq -c | sort -rn
```

### 游戏统计
```bash
# 统计创建的游戏数
grep "Game created" logs/catamaze.log | wc -l

# 统计游戏结果
grep "Game.*ended" logs/catamaze.log | grep "won" | wc -l
grep "Game.*ended" logs/catamaze.log | grep "lost" | wc -l
```

## 最佳实践

### 1. 使用结构化日志
```python
# 不好
logger.info("Player moved to 10 20")

# 好
logger.info(f"Player moved to ({x}, {y})", extra={
    'game_id': game_id,
    'entity_id': entity_id,
    'position': {'x': x, 'y': y}
})
```

### 2. 避免敏感信息
```python
# 不要记录敏感信息
logger.debug(f"Database URL: {DATABASE_URL}")  # ❌

# 只记录必要信息
logger.debug("Database connected")  # ✅
```

### 3. 使用上下文管理
```python
import logging
from contextlib import contextmanager

@contextmanager
def log_context(game_id):
    logger = logging.LoggerAdapter(
        logging.getLogger(__name__),
        {'game_id': game_id}
    )
    yield logger

with log_context("abc123") as logger:
    logger.info("Processing game")  # 自动包含game_id
```

### 4. 日志轮转
```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    'logs/catamaze.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5  # 保留5个备份
)
```

### 5. 异步日志（高性能）
```python
from logging.handlers import QueueHandler, QueueListener
import queue
import logging

log_queue = queue.Queue(-1)
queue_handler = QueueHandler(log_queue)

handler = logging.FileHandler('logs/catamaze.log')
listener = QueueListener(log_queue, handler)
listener.start()

logger = logging.getLogger()
logger.addHandler(queue_handler)
```

## 监控和告警

### 错误率监控
```python
import logging
from collections import defaultdict
import time

class ErrorRateMonitor(logging.Handler):
    def __init__(self):
        super().__init__()
        self.error_counts = defaultdict(int)
        self.last_check = time.time()

    def emit(self, record):
        if record.levelno >= logging.ERROR:
            self.error_counts[record.name] += 1

            # 每分钟检查一次
            if time.time() - self.last_check > 60:
                self.check_error_rate()
                self.last_check = time.time()

    def check_error_rate(self):
        for name, count in self.error_counts.items():
            if count > 10:
                # 发送告警
                logger.critical(f"High error rate in {name}: {count} errors/min")

monitor = ErrorRateMonitor()
logging.getLogger().addHandler(monitor)
```

---

**相关文档**:
- `docs/errors.md` - 错误处理
- `docs/performance.md` - 性能优化
