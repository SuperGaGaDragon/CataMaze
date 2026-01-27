# Performance Optimization

CataMaze性能优化指南和最佳实践。

## 性能指标

### 目标性能
- **API响应时间**: <100ms (p95)
- **Tick处理时间**: <50ms
- **并发游戏数**: 50+
- **数据库查询**: <10ms (简单查询)
- **内存使用**: <2GB (50个并发游戏)

### 当前性能
- API响应: 20-50ms (typical)
- Tick处理: 10-30ms
- 数据库查询: 5-15ms
- 内存使用: ~500MB (10个游戏)

## Backend优化

### 1. 数据库优化

#### 索引优化
```python
# backend/storage/models.py
class GameState(Base):
    __tablename__ = 'game_states'

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(String, unique=True, index=True)  # 索引
    tick = Column(Integer, index=True)  # 索引用于按时间查询

class EventLog(Base):
    __tablename__ = 'event_logs'

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(String, index=True)  # 索引
    tick = Column(Integer, index=True)  # 复合索引
```

#### 查询优化
```python
# 不好 - N+1查询
for game_id in game_ids:
    game = session.query(GameState).filter_by(game_id=game_id).first()

# 好 - 批量查询
games = session.query(GameState).filter(
    GameState.game_id.in_(game_ids)
).all()
```

#### 连接池
```python
# backend/storage/db.py
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,  # 连接池大小
    max_overflow=20,  # 最大溢出连接数
    pool_pre_ping=True,  # 检查连接有效性
    pool_recycle=3600  # 1小时回收连接
)
```

### 2. 缓存策略

#### 内存缓存（游戏状态）
```python
from functools import lru_cache

class GameManager:
    def __init__(self):
        self.game_cache = {}  # 活跃游戏缓存

    def get_game(self, game_id):
        # 先查缓存
        if game_id in self.game_cache:
            return self.game_cache[game_id]

        # 再查数据库
        game = load_from_db(game_id)
        self.game_cache[game_id] = game
        return game

    def save_game(self, game):
        # 更新缓存
        self.game_cache[game.game_id] = game
        # 异步写数据库
        save_to_db_async(game)
```

#### LRU缓存
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def load_map(map_name):
    """缓存地图数据"""
    with open(f"maps/{map_name}.txt", 'r') as f:
        return f.read()
```

### 3. 异步处理

#### 异步数据库操作
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)

async def save_game_async(game_state):
    """异步保存游戏状态"""
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(executor, save_to_db, game_state)
```

#### 后台任务
```python
from fastapi import BackgroundTasks

@app.post("/game/tick")
def tick_game(game_id: str, background_tasks: BackgroundTasks):
    # 处理tick
    result = process_tick(game_id)

    # 异步保存日志
    background_tasks.add_task(save_event_log, game_id, result.events)

    return result
```

### 4. 批处理

#### 批量保存事件
```python
class EventBuffer:
    def __init__(self, flush_size=100):
        self.buffer = []
        self.flush_size = flush_size

    def add_event(self, event):
        self.buffer.append(event)
        if len(self.buffer) >= self.flush_size:
            self.flush()

    def flush(self):
        if self.buffer:
            # 批量插入
            session.bulk_insert_mappings(EventLog, self.buffer)
            session.commit()
            self.buffer.clear()
```

## Frontend优化

### 1. Terminal优化

#### 减少渲染频率
```typescript
// frontend/terminal/renderer.ts
class Renderer {
  private lastRenderTime = 0;
  private renderInterval = 50; // 最多20fps

  render(state: GameState) {
    const now = Date.now();
    if (now - this.lastRenderTime < this.renderInterval) {
      return; // 跳过渲染
    }

    this.doRender(state);
    this.lastRenderTime = now;
  }
}
```

#### 增量更新
```typescript
// 只更新变化的部分
class IncrementalRenderer {
  private lastState: GameState | null = null;

  render(state: GameState) {
    if (!this.lastState) {
      this.fullRender(state);
    } else {
      this.renderDiff(this.lastState, state);
    }
    this.lastState = state;
  }

  renderDiff(oldState: GameState, newState: GameState) {
    // 只渲染变化的单元格
    for (let y = 0; y < 5; y++) {
      for (let x = 0; x < 5; x++) {
        if (oldState.vision[y][x] !== newState.vision[y][x]) {
          this.renderCell(x, y, newState.vision[y][x]);
        }
      }
    }
  }
}
```

### 2. UI优化

#### DOM最小化更新
```javascript
// frontend/UI/renderer.js
function updateHUD(hp, ammo) {
  // 只在值变化时更新
  const hpElement = document.getElementById('hp-value');
  if (hpElement.textContent !== hp.toString()) {
    hpElement.textContent = hp;
  }

  const ammoElement = document.getElementById('ammo-value');
  if (ammoElement.textContent !== ammo.toString()) {
    ammoElement.textContent = ammo;
  }
}
```

#### 使用DocumentFragment
```javascript
// 批量DOM操作
function renderEvents(events) {
  const fragment = document.createDocumentFragment();

  events.forEach(event => {
    const div = document.createElement('div');
    div.textContent = event;
    fragment.appendChild(div);
  });

  // 一次性插入
  document.getElementById('event-log').appendChild(fragment);
}
```

#### 虚拟滚动
```javascript
// 事件日志虚拟滚动
class VirtualEventLog {
  constructor(maxVisible = 10) {
    this.maxVisible = maxVisible;
    this.allEvents = [];
  }

  addEvent(event) {
    this.allEvents.push(event);

    // 只保留最后N条在DOM中
    if (this.allEvents.length > this.maxVisible) {
      this.allEvents.shift();
    }

    this.render();
  }
}
```

## 算法优化

### 1. 路径查找优化
```python
# backend/engine/pathfinding.py
from functools import lru_cache

@lru_cache(maxsize=1000)
def find_path(start, end, map_hash):
    """缓存路径查找结果"""
    # A*算法实现
    pass

# 使用时传入地图哈希值以支持缓存
map_hash = hash(tuple(map(tuple, game_map)))
path = find_path((x1, y1), (x2, y2), map_hash)
```

### 2. 碰撞检测优化
```python
# 空间哈希
class SpatialHash:
    def __init__(self, cell_size=10):
        self.cell_size = cell_size
        self.grid = {}

    def insert(self, entity):
        cell = self.get_cell(entity.x, entity.y)
        if cell not in self.grid:
            self.grid[cell] = []
        self.grid[cell].append(entity)

    def get_nearby(self, x, y, radius=2):
        """只检查附近单元格的实体"""
        entities = []
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                cell = self.get_cell(x + dx * self.cell_size,
                                     y + dy * self.cell_size)
                entities.extend(self.grid.get(cell, []))
        return entities
```

### 3. 视野计算优化
```python
# 预计算视野模板
VISION_TEMPLATE = precompute_vision_offsets(radius=2)

def get_vision(center_x, center_y, game_map):
    """使用预计算的偏移量"""
    vision = []
    for dx, dy in VISION_TEMPLATE:
        x, y = center_x + dx, center_y + dy
        if 0 <= x < 50 and 0 <= y < 50:
            vision.append(game_map[y][x])
    return vision
```

## 监控和分析

### 1. 性能监控
```python
import time
from contextlib import contextmanager

@contextmanager
def timer(name):
    start = time.time()
    yield
    elapsed = time.time() - start
    logger.debug(f"{name} took {elapsed*1000:.2f}ms")

# 使用
with timer("process_tick"):
    game.tick()
```

### 2. 内存分析
```python
import tracemalloc

tracemalloc.start()

# 执行操作
game.tick()

# 查看内存使用
current, peak = tracemalloc.get_traced_memory()
print(f"Current: {current / 1024 / 1024:.2f}MB")
print(f"Peak: {peak / 1024 / 1024:.2f}MB")

tracemalloc.stop()
```

### 3. Profiling
```python
import cProfile
import pstats

# Profile代码
profiler = cProfile.Profile()
profiler.enable()

game.tick()

profiler.disable()

# 输出结果
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)  # 前10个最慢的函数
```

## 配置优化

### 生产环境配置
```python
# config/production.py
CONFIG = {
    # 数据库
    "db_pool_size": 20,
    "db_max_overflow": 40,

    # 缓存
    "game_cache_size": 100,
    "map_cache_size": 50,

    # 并发
    "max_games": 50,
    "worker_threads": 4,

    # 性能
    "enable_profiling": False,
    "enable_debug_logs": False,
}
```

### 开发环境配置
```python
# config/development.py
CONFIG = {
    "db_pool_size": 5,
    "game_cache_size": 10,
    "max_games": 10,
    "enable_profiling": True,
    "enable_debug_logs": True,
}
```

## 性能检查清单

- [ ] 数据库查询使用索引
- [ ] 实现连接池
- [ ] 缓存常用数据（地图、游戏状态）
- [ ] 异步处理非关键操作
- [ ] 批量处理数据库写入
- [ ] Frontend增量渲染
- [ ] 限制DOM更新频率
- [ ] 使用性能监控
- [ ] 定期Profiling
- [ ] 负载测试

---

**相关文档**:
- `docs/logging.md` - 日志系统
- `docs/api_spec.md` - API规范
