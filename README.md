# CataMaze

一个基于强化学习的生存迷宫游戏。玩家在50x50的迷宫中生存，使用有限的视野和弹药对抗AI敌人。

## 特性

- 🎮 **回合制生存游戏**: 在迷宫中探索、战斗、生存
- 👁️ **局部视野**: 5x5有限视野，增加探索挑战
- 🔫 **战术射击**: 弹药系统 (3发最大，自动恢复)
- ❤️ **生命值**: HP系统 (5点最大)
- 🔊 **音频系统**: 听声辨位，感知敌人
- 🤖 **AI代理**: 多种人格（进攻/谨慎/探索）
- 🖥️ **多界面**: Terminal CLI + Web UI
- 💾 **数据持久化**: PostgreSQL/SQLite支持
- 🔍 **开发者模式**: Watch模式查看完整地图

## 快速开始

### 环境要求

- Python 3.9+
- Node.js 14+ (可选，用于TypeScript编译)
- PostgreSQL (生产环境) 或 SQLite (开发环境)

### 安装

```bash
# 克隆仓库
git clone https://github.com/SuperGaGaDragon/CataMaze.git
cd CataMaze

# 安装Python依赖
pip install -r requirements.txt

# 设置数据库 (可选，默认使用SQLite)
export DATABASE_URL="postgresql://user:pass@localhost/catamaze"

# 初始化数据库
python -c "from backend.storage.db import init_db; init_db()"
```

### 启动服务器

```bash
# 启动FastAPI服务器
uvicorn backend.api.routes:app --reload --port 8000
```

服务器运行在 `http://localhost:8000`

### 使用Terminal界面

```bash
# 安装terminal CLI (如果使用TypeScript)
cd frontend/terminal
npm install
npm run build

# 或直接使用Python脚本
python frontend/terminal/catamaze_cli.py new --map default
python frontend/terminal/catamaze_cli.py move north --game-id <game_id>
python frontend/terminal/catamaze_cli.py shoot east --game-id <game_id>
```

### 使用Web界面

```bash
# 在浏览器中打开
open frontend/UI/index.html

# 或使用简单HTTP服务器
cd frontend/UI
python -m http.server 8080
```

访问 `http://localhost:8080`

## 游戏玩法

### 目标
在迷宫中生存并消灭所有敌人。

### 控制

**Terminal**:
- `catamaze new` - 创建新游戏
- `catamaze move <direction>` - 移动 (north/south/east/west)
- `catamaze shoot <direction>` - 射击
- `catamaze observe` - 查看当前状态
- `catamaze tick` - 推进游戏时间

**Web UI**:
- WASD - 移动
- IJKL - 射击
- 点击按钮 - 执行动作

### 游戏机制

- **HP**: 5点生命值，归零则失败
- **弹药**: 最多3发，每2 tick自动恢复1发
- **视野**: 5x5局部视野，墙壁阻挡视线
- **音频**: 听到射击声可判断敌人方位
- **子弹**: 每tick移动1格，击中墙壁消失

### 地图符号

```
@ - 玩家
E - 敌人
# - 墙壁
. - 空地
H - 生命包
A - 弹药包
* - 子弹
```

## API文档

完整API文档见 [docs/api_spec.md](docs/api_spec.md)

### 核心端点

```bash
# 创建游戏
POST /game/new
{
  "map_name": "default"
}

# 执行动作
POST /game/action
{
  "game_id": "abc123",
  "action": "move_north"
}

# 推进时间
POST /game/tick
{
  "game_id": "abc123"
}

# 观察游戏
GET /game/observe?game_id=abc123

# Watch模式 (开发者)
GET /game/watch?game_id=abc123-watch
```

## 项目结构

```
catamaze/
├── backend/
│   ├── engine/         # 游戏引擎核心
│   │   ├── game.py           # 游戏主类
│   │   ├── entity.py         # 实体系统
│   │   ├── bullet.py         # 子弹物理
│   │   ├── observation.py    # 观察生成
│   │   └── sound.py          # 音频系统
│   ├── api/            # REST API
│   │   └── routes.py         # API端点
│   ├── storage/        # 数据库层
│   │   ├── db.py             # 数据库连接
│   │   ├── models.py         # 数据模型
│   │   └── repository.py     # 数据访问
│   └── agents/         # AI代理
│       ├── base.py           # 基类
│       ├── human.py          # 人类代理
│       ├── registry.py       # 注册系统
│       └── rl/               # RL代理
│           ├── agent.py      # RL代理主类
│           ├── encoder.py    # 观察编码
│           ├── policy.py     # 策略
│           ├── reward.py     # 奖励计算
│           └── action_mask.py # 动作掩码
├── frontend/
│   ├── terminal/       # CLI界面
│   │   └── catamaze_cli.py
│   └── UI/             # Web界面
│       ├── index.html
│       ├── style.css
│       └── game.js
├── maps/               # 地图文件
│   └── default.txt
├── docs/               # 文档
│   ├── api_spec.md
│   ├── terminal_usage.md
│   ├── watch_mode.md
│   ├── personas.md
│   └── ...
└── README.md
```

## AI Persona系统

CataMaze支持多种AI人格：

### Aggressive (进攻型)
```json
{
  "shoot_probability": 0.7,
  "chase_probability": 0.8,
  "explore_probability": 0.2,
  "flee_probability": 0.1
}
```

### Cautious (谨慎型)
```json
{
  "shoot_probability": 0.2,
  "chase_probability": 0.3,
  "explore_probability": 0.7,
  "flee_probability": 0.8
}
```

### Explorer (探索型)
```json
{
  "shoot_probability": 0.1,
  "chase_probability": 0.1,
  "explore_probability": 0.9,
  "flee_probability": 0.5
}
```

详细说明见 [docs/personas.md](docs/personas.md)

## 开发

### 运行测试

```bash
# 安装测试依赖
pip install pytest pytest-cov

# 运行所有测试
pytest

# 带覆盖率
pytest --cov=backend --cov-report=html
```

### 代码规范

- 所有文件 <200 lines
- 使用类型提示
- 文档字符串
- 错误处理

详见 [docs/dev_rules.md](docs/dev_rules.md)

### 添加新地图

```bash
# 创建地图文件
cat > maps/my_map.txt << EOF
################
#..............#
#..E...........#
#..........@...#
#..............#
################
EOF

# 使用新地图
catamaze new --map my_map
```

## 性能

- **API响应**: <100ms (p95)
- **并发游戏**: 50+
- **内存使用**: ~500MB (10游戏)

优化指南见 [docs/performance.md](docs/performance.md)

## 故障排除

### 数据库连接失败
```bash
# 检查DATABASE_URL
echo $DATABASE_URL

# 测试连接
python -c "from backend.storage.db import test_connection; print(test_connection())"
```

### API 404错误
```bash
# 确认服务器运行
curl http://localhost:8000/

# 检查game_id是否正确
catamaze observe --game-id <game_id>
```

### Watch模式403错误
```bash
# 确保game_id以-watch结尾
curl "http://localhost:8000/game/watch?game_id=abc123-watch"
```

更多错误处理见 [docs/errors.md](docs/errors.md)

## 文档

- [API规范](docs/api_spec.md) - 完整API文档
- [Terminal使用](docs/terminal_usage.md) - CLI指南
- [Watch模式](docs/watch_mode.md) - 开发者工具
- [数据模型](docs/data_models.md) - 数据结构
- [Persona系统](docs/personas.md) - AI人格
- [错误处理](docs/errors.md) - 错误码和处理
- [日志系统](docs/logging.md) - 日志配置
- [性能优化](docs/performance.md) - 优化指南
- [开发规范](docs/dev_rules.md) - 代码规范
- [发布说明](docs/release_notes.md) - 版本历史

## 路线图

### v1.1.0
- [ ] RL Agent训练 (PPO/DQN)
- [ ] Redis缓存
- [ ] WebSocket支持
- [ ] 回放系统

### v1.2.0
- [ ] 多人游戏
- [ ] 地图编辑器
- [ ] 排行榜
- [ ] 移动端适配

### v2.0.0
- [ ] 技能系统
- [ ] 装备系统
- [ ] 关卡系统
- [ ] 社区功能

## 贡献

欢迎贡献！请遵循以下步骤：

1. Fork仓库
2. 创建功能分支 (`git checkout -b feature/amazing`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing`)
5. 开启Pull Request

## 许可证

MIT License - 详见 LICENSE 文件

## 联系方式

- GitHub: [SuperGaGaDragon/CataMaze](https://github.com/SuperGaGaDragon/CataMaze)
- Issues: [GitHub Issues](https://github.com/SuperGaGaDragon/CataMaze/issues)

## 致谢

感谢所有为CataMaze做出贡献的开发者！

---

**版本**: 1.0.0
**最后更新**: 2026-01-27
**状态**: ✅ Production Ready
