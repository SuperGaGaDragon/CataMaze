# Agent Personas

CataMaze支持多种AI代理人格，每种人格具有不同的行为特征和决策模式。

## 人格系统架构

### 配置文件位置
```
backend/personas/
├── aggressive.json
├── cautious.json
└── explorer.json
```

### 配置文件结构
```json
{
  "name": "persona_name",
  "description": "Persona description",
  "behavior": {
    "shoot_probability": 0.0-1.0,
    "chase_probability": 0.0-1.0,
    "explore_probability": 0.0-1.0,
    "flee_probability": 0.0-1.0
  },
  "decision_weights": {
    "attack": 0.0-1.0,
    "chase": 0.0-1.0,
    "explore": 0.0-1.0,
    "flee": 0.0-1.0
  },
  "thresholds": {
    "min_hp_to_attack": int,
    "max_distance_to_chase": int,
    "ammo_conservation": 0.0-1.0,
    "flee_hp_threshold": int
  }
}
```

## 可用人格

### 1. Aggressive (进攻型)
**特征**: 主动追击玩家，高攻击倾向

**配置**:
- `shoot_probability`: 0.7 - 高射击倾向
- `chase_probability`: 0.8 - 积极追击
- `explore_probability`: 0.2 - 较少探索
- `flee_probability`: 0.1 - 很少逃跑

**决策权重**:
- `attack`: 0.6 - 优先攻击
- `chase`: 0.3 - 追击次优先
- `explore`: 0.1 - 探索最低

**阈值**:
- `min_hp_to_attack`: 2 - 低血量仍攻击
- `max_distance_to_chase`: 15 - 追击距离远
- `ammo_conservation`: 0.3 - 不保守弹药

**适用场景**:
- Boss级敌人
- 高难度关卡
- 需要压迫感的场景

### 2. Cautious (谨慎型)
**特征**: 避免冲突，优先生存

**配置**:
- `shoot_probability`: 0.2 - 低射击倾向
- `chase_probability`: 0.3 - 谨慎追击
- `explore_probability`: 0.7 - 较多探索
- `flee_probability`: 0.8 - 高逃跑倾向

**决策权重**:
- `attack`: 0.1 - 很少攻击
- `chase`: 0.2 - 很少追击
- `explore`: 0.4 - 探索为主
- `flee`: 0.3 - 逃跑权重高

**阈值**:
- `min_hp_to_attack`: 4 - 高血量才攻击
- `max_distance_to_chase`: 5 - 追击距离近
- `ammo_conservation`: 0.8 - 保守弹药
- `flee_hp_threshold`: 3 - 血量≤3时逃跑

**适用场景**:
- 辅助型敌人
- 新手关卡
- 平衡游戏难度

### 3. Explorer (探索型)
**特征**: 专注地图探索和发现

**配置**:
- `shoot_probability`: 0.1 - 极少射击
- `chase_probability`: 0.1 - 极少追击
- `explore_probability`: 0.9 - 极高探索
- `flee_probability`: 0.5 - 中等逃跑

**决策权重**:
- `attack`: 0.05 - 极少攻击
- `chase`: 0.05 - 极少追击
- `explore`: 0.8 - 探索为核心
- `flee`: 0.1 - 适度逃跑

**阈值**:
- `min_hp_to_attack`: 3 - 中等血量才攻击
- `max_distance_to_chase`: 3 - 追击距离很近
- `ammo_conservation`: 0.9 - 极度保守弹药
- `exploration_priority`: 0.9 - 探索优先级极高

**适用场景**:
- 游荡型NPC
- 地图控制角色
- 非战斗场景

## 使用方法

### 创建带人格的代理
```python
from backend.agents.rl.agent import RLAgent

# 创建进攻型代理
aggressive_agent = RLAgent(entity_id="enemy_1", persona="aggressive")

# 创建谨慎型代理
cautious_agent = RLAgent(entity_id="enemy_2", persona="cautious")

# 创建探索型代理
explorer_agent = RLAgent(entity_id="enemy_3", persona="explorer")
```

### 自定义人格
1. 在 `backend/personas/` 创建新JSON文件
2. 定义行为参数、决策权重、阈值
3. 使用人格名称创建代理

示例 - `backend/personas/sniper.json`:
```json
{
  "name": "sniper",
  "description": "Long-range attacker that avoids close combat",
  "behavior": {
    "shoot_probability": 0.9,
    "chase_probability": 0.2,
    "explore_probability": 0.3,
    "flee_probability": 0.6
  },
  "decision_weights": {
    "attack": 0.7,
    "chase": 0.1,
    "explore": 0.1,
    "flee": 0.1
  },
  "thresholds": {
    "min_hp_to_attack": 3,
    "max_distance_to_chase": 8,
    "ammo_conservation": 0.5,
    "min_shoot_distance": 5
  }
}
```

## 人格系统实现

### RL代理集成
`backend/agents/rl/agent.py` 中的 `RLAgent` 类在初始化时加载人格配置：

```python
def __init__(self, entity_id: str, persona: str = "aggressive"):
    persona_path = f"backend/personas/{persona}.json"
    if os.path.exists(persona_path):
        with open(persona_path, 'r') as f:
            self.persona_config = json.load(f)
```

### 决策流程
1. **观察编码**: `ObservationEncoder` 将游戏状态编码为特征向量
2. **动作掩码**: `ActionMask` 确定当前可用动作
3. **策略选择**: `Policy` 根据人格配置和特征选择动作
4. **奖励计算**: `RewardCalculator` 计算行为奖励用于训练

### 人格影响决策
在 `backend/agents/rl/policy.py` 的 `select_action` 方法中：

```python
def select_action(self, features, valid_actions, persona_config):
    # 获取人格参数
    behavior = persona_config.get("behavior", {})
    decision_weights = persona_config.get("decision_weights", {})
    thresholds = persona_config.get("thresholds", {})

    # 基于人格计算动作分数
    action_scores = self._compute_action_scores(
        features, valid_actions, persona_config
    )

    # 选择动作
    return self._select_from_scores(action_scores)
```

## 最佳实践

1. **平衡性**: 确保决策权重总和合理，避免单一行为占主导
2. **阈值调整**: 根据游戏难度调整HP、距离等阈值
3. **测试**: 每个新人格都应进行充分测试
4. **文档**: 为自定义人格编写清晰的描述

---

**相关文档**:
- `docs/api_spec.md` - API规范
- `docs/data_models.md` - 数据模型
- `backend/agents/rl/agent.py` - RL代理实现
