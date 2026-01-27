# Error Handling

CataMaze API的错误处理机制和错误码规范。

## HTTP状态码

### 400 Bad Request
**原因**: 请求参数无效

**常见场景**:
- 缺少必需参数
- 参数格式错误
- 无效的动作字符串

**响应格式**:
```json
{
  "error": "Invalid action",
  "details": "Action 'invalid_move' is not recognized"
}
```

**示例**:
```bash
# 无效动作
curl -X POST http://localhost:8000/game/action \
  -H "Content-Type: application/json" \
  -d '{"game_id": "abc", "action": "invalid_move"}'

# Response: 400
{
  "error": "Invalid action",
  "details": "Action must be one of: move_north, move_south, ..."
}
```

### 403 Forbidden
**原因**: 权限不足或访问被拒绝

**常见场景**:
- Watch模式game_id缺少 `-watch` 后缀
- 尝试访问不允许的资源

**响应格式**:
```json
{
  "error": "Watch mode required",
  "details": "Use game_id with '-watch' suffix"
}
```

**示例**:
```bash
# 没有-watch后缀访问watch端点
curl "http://localhost:8000/game/watch?game_id=abc"

# Response: 403
{
  "error": "Watch mode required",
  "details": "Watch mode game_id must end with '-watch'"
}
```

### 404 Not Found
**原因**: 游戏不存在

**常见场景**:
- game_id不存在或已删除
- 拼写错误的game_id

**响应格式**:
```json
{
  "error": "Game not found",
  "game_id": "nonexistent"
}
```

**示例**:
```bash
# 不存在的game_id
curl "http://localhost:8000/game/observe?game_id=nonexistent"

# Response: 404
{
  "error": "Game not found",
  "game_id": "nonexistent"
}
```

### 503 Service Unavailable
**原因**: 服务器超载

**常见场景**:
- 并发游戏数超过限制（50个）
- 服务器资源不足

**响应格式**:
```json
{
  "error": "Too many active games",
  "limit": 50,
  "current": 50
}
```

**示例**:
```bash
# 第51个游戏创建请求
curl -X POST http://localhost:8000/game/new \
  -H "Content-Type: application/json" \
  -d '{"map_name": "default"}'

# Response: 503
{
  "error": "Too many active games",
  "limit": 50,
  "current": 50,
  "message": "Please try again later"
}
```

## 游戏状态错误

### Game Over
**原因**: 游戏已结束

**检测方法**:
```python
response = requests.post("http://localhost:8000/game/action", json={
    "game_id": game_id,
    "action": "move_north"
})

data = response.json()
if data.get("status") in ["won", "lost"]:
    print("Game is over:", data["status"])
```

**响应示例**:
```json
{
  "observation": {...},
  "status": "lost",
  "message": "You died!",
  "final_tick": 156
}
```

### Invalid Action
**原因**: 动作在当前状态下不可用

**常见场景**:
- 向墙壁移动
- 弹药为0时射击
- HP为0时行动

**处理方法**:
```python
# 检查有效动作
observation = get_observation(game_id)
valid_actions = get_valid_actions(observation)

if action not in valid_actions:
    print(f"Action {action} is not valid")
```

## 网络错误

### Connection Error
**原因**: 无法连接到服务器

**处理示例**:
```python
import requests
from requests.exceptions import ConnectionError

try:
    response = requests.get("http://localhost:8000/game/observe?game_id=abc")
except ConnectionError as e:
    print("Cannot connect to server:", e)
    # 重试逻辑
```

### Timeout
**原因**: 请求超时

**处理示例**:
```python
try:
    response = requests.post(
        "http://localhost:8000/game/tick",
        json={"game_id": game_id},
        timeout=5.0  # 5秒超时
    )
except requests.Timeout:
    print("Request timed out")
```

## 错误处理最佳实践

### 1. 使用Try-Except包装API调用
```python
def safe_api_call(url, method="GET", **kwargs):
    try:
        if method == "GET":
            response = requests.get(url, **kwargs)
        else:
            response = requests.post(url, **kwargs)

        response.raise_for_status()
        return response.json()

    except requests.ConnectionError:
        print("Connection failed")
        return None
    except requests.Timeout:
        print("Request timeout")
        return None
    except requests.HTTPError as e:
        print(f"HTTP error: {e.response.status_code}")
        return None
```

### 2. 检查响应状态
```python
response = requests.post(url, json=data)

if response.status_code == 200:
    # 成功
    data = response.json()
elif response.status_code == 400:
    # 参数错误
    error = response.json()
    print("Bad request:", error["details"])
elif response.status_code == 404:
    # 游戏不存在
    print("Game not found")
elif response.status_code == 503:
    # 服务器超载
    print("Server is busy, retry later")
```

### 3. 重试机制
```python
import time

def api_call_with_retry(url, max_retries=3, delay=1.0):
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=data)
            if response.status_code == 503:
                # 服务器超载，等待后重试
                time.sleep(delay * (attempt + 1))
                continue
            return response.json()
        except requests.ConnectionError:
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                raise
```

### 4. 日志记录
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    response = requests.post(url, json=data)
    response.raise_for_status()
except requests.HTTPError as e:
    logger.error(f"API error: {e.response.status_code} - {e.response.text}")
except Exception as e:
    logger.exception("Unexpected error")
```

## 常见问题

### Q: 如何处理游戏已结束的情况？
A: 检查响应中的 `status` 字段：
```python
data = response.json()
if data.get("status") in ["won", "lost"]:
    print("Game over:", data.get("message"))
    # 清理资源或开始新游戏
```

### Q: 如何避免503错误？
A:
1. 限制客户端同时创建的游戏数量
2. 游戏结束后及时清理
3. 实现重试机制

### Q: Watch模式403错误如何解决？
A: 确保game_id以 `-watch` 结尾：
```python
# 错误
game_id = "abc123"

# 正确
game_id = "abc123-watch"
```

---

**相关文档**:
- `docs/api_spec.md` - API完整规范
- `docs/logging.md` - 日志系统
