# CataMaze Integration with CataChess

CataMaze现已集成到CataChess伪终端系统！

## ✅ 已完成的集成

### 1. 符号链接
```bash
~/Desktop/catachess/patch/modules/catamaze -> ~/Desktop/catamaze/frontend/terminal
```

### 2. 模块注册
在 `catachess/patch/index.ts` 中已添加：
```typescript
// CataMaze Game
export { CataMazeTerminal, createCataMazeCommand } from './modules/catamaze';
export type { Observation, GameStateResponse } from './modules/catamaze';
```

## 🎮 如何使用

### 方式1：直接组件（推荐用于独立页面）

在CataChess的任何React组件中：

```typescript
import { CataMazeTerminal } from '@patch';

function GamePage() {
  return <CataMazeTerminal />;
}
```

### 方式2：命令集成（推荐用于终端内使用）

在现有Terminal中添加CataMaze命令：

```typescript
import { TerminalLauncher } from '@patch/modules/terminal';
import { createCataMazeCommand } from '@patch/modules/catamaze';
import { useRef } from 'react';

function MyTerminal() {
  const gameState = useRef({
    gameId: null,
    observation: null,
    queueSize: 0,
  });

  const cataMazeCommand = createCataMazeCommand(gameState);

  return (
    <TerminalLauncher
      initialSystem="dos"
      customCommands={[cataMazeCommand]}
    />
  );
}
```

## 🎯 终端命令

一旦集成，在CataChess终端中可以使用：

```bash
# 创建新游戏
catamaze new

# 执行动作（移动）
catamaze action move_north
catamaze a move_south      # 简写

# 执行动作（射击）
catamaze action shoot_east
catamaze a shoot_west      # 简写

# 推进游戏
catamaze tick
catamaze t                 # 简写

# 查看状态
catamaze observe
catamaze o                 # 简写

# 查看队列
catamaze queue
catamaze q                 # 简写

# 清空队列
catamaze clear
catamaze esc               # 简写

# 恢复游戏
catamaze resume <game_id>
catamaze r <game_id>       # 简写

# 帮助
catamaze help
```

**别名**: `cm`, `cata`

示例：
```bash
cm new
cm a move_north
cm t
cm o
```

## 🔧 前置要求

### 1. 启动CataMaze API服务器

**本地开发**:
```bash
cd ~/Desktop/catamaze
uvicorn backend.api.routes:app --reload --port 8000
```

**或使用Railway部署的URL**:
- 在 `frontend/terminal/apiClient.ts` 中修改 `API_BASE_URL`
- 设置为你的Railway URL

### 2. 配置API URL（如果需要）

编辑 `catamaze/frontend/terminal/apiClient.ts`:
```typescript
const API_BASE_URL = process.env.CATAMAZE_API_URL || 'http://localhost:8000';
```

或设置环境变量：
```bash
export CATAMAZE_API_URL="https://your-railway-url"
```

## 📊 游戏界面

终端会显示ASCII艺术界面：

```
╔═══ TICK 42 ════════════════════╗
║ HP: ♥♥♥♥♥  Ammo: ●●○           ║
║ Time: 42  Pos: (25,30)         ║
╠════════════════════════════════╣
║          VISION (5x5)          ║
╠════════════════════════════════╣
║    # # # # #                   ║
║    # . . E #                   ║
║    # . @ . #                   ║
║    # . . . #                   ║
║    # # # # #                   ║
╠════════════════════════════════╣
║ Sound: Gunshot from NORTH      ║
╠════════════════════════════════╣
║ ✓ Alive  - Playing             ║
╚════════════════════════════════╝
```

## 🎨 地图符号

- `@` - 玩家
- `E` - 敌人
- `#` - 墙壁
- `.` - 空地
- `H` - 生命包
- `A` - 弹药包
- `*` - 子弹

## 🚀 快速测试

1. **启动API服务器**:
   ```bash
   cd ~/Desktop/catamaze
   uvicorn backend.api.routes:app --port 8000
   ```

2. **在CataChess中使用**:
   - 打开CataChess开发环境
   - 导入并使用 `<CataMazeTerminal />` 组件
   - 或在现有终端中添加 `catamaze` 命令

3. **开始游戏**:
   ```bash
   catamaze new
   catamaze a move_north
   catamaze t
   catamaze o
   ```

## 📝 开发注意事项

- **自动同步**: 符号链接意味着对 `catamaze/frontend/terminal/` 的任何更改会立即反映在CataChess中
- **类型安全**: 所有导出都有TypeScript类型定义
- **命令别名**: 支持简写命令提高效率
- **状态管理**: 游戏状态通过useRef在组件间共享

## 🔍 故障排除

### Terminal找不到catamaze命令
- 检查符号链接: `ls -la ~/Desktop/catachess/patch/modules/catamaze`
- 检查 `catachess/patch/index.ts` 是否有CataMaze导出

### API连接失败
- 确认服务器运行: `curl http://localhost:8000/`
- 检查API_BASE_URL配置
- 查看浏览器Console错误

### TypeScript错误
- 重新构建CataChess: `npm run build`
- 检查导入路径是否正确

## 📚 相关文档

- [CataMaze README](README.md)
- [Terminal使用指南](docs/terminal_usage.md)
- [API规范](docs/api_spec.md)

---

**集成完成时间**: 2026-01-27
**状态**: ✅ Ready to Use
