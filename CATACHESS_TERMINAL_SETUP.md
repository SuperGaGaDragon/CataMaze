# CataChess 伪终端 CataMaze 命令设置

## ✅ 已完成的集成

### 1. 命令已注册
在 CataChess 代码库中：
- ✅ 创建了 `patch/modules/terminal/frontend/commands/catamaze.ts`
- ✅ 在 `patch/modules/terminal/frontend/commands/index.ts` 中注册了命令
- ✅ 已推送到 GitHub: commit `9b041af`

### 2. API已部署
- ✅ URL: https://catamaze.catachess.com
- ✅ 所有端点测试通过
- ✅ 数据库已连接并初始化

## 🔨 如何启用命令

### 方法1: 重新构建 CataChess (推荐)

```bash
cd ~/Desktop/catachess

# 拉取最新代码 (如果需要)
git pull

# 安装依赖 (如果还没有)
npm install

# 重新构建
npm run build

# 或者如果是开发模式
npm run dev
```

### 方法2: 热重载 (如果开发服务器正在运行)

如果你的 CataChess 开发服务器 (Vite) 正在运行：
1. 保存文件后应该自动热重载
2. 刷新浏览器页面
3. 按 F12 打开终端
4. 输入 `catamaze help`

### 方法3: 清除缓存并重启

```bash
cd ~/Desktop/catachess

# 清除构建缓存
rm -rf node_modules/.vite
rm -rf dist

# 重新构建
npm run build

# 重启开发服务器
npm run dev
```

## 🎮 使用 CataMaze 命令

### 打开终端
- 按 **F12** 键
- 或按 **Ctrl + `**
- 或点击右下角的终端图标

### 命令列表

```bash
# 创建新游戏
catamaze new

# 添加动作 (简写: catamaze a)
catamaze action MOVE_UP
catamaze a MOVE_DOWN
catamaze a SHOOT_RIGHT

# 执行tick (简写: catamaze t)
catamaze tick
catamaze t

# 查看状态 (简写: catamaze o)
catamaze observe
catamaze o

# 查看队列 (简写: catamaze q)
catamaze queue
catamaze q

# 清空队列 (简写: catamaze esc)
catamaze clear
catamaze esc

# 恢复游戏 (简写: catamaze r)
catamaze resume <game_id>
catamaze r <game_id>

# 显示帮助
catamaze help
```

### 使用别名

```bash
# 使用 cm 别名
cm new
cm a MOVE_UP
cm t
cm o

# 使用 cata 别名
cata new
cata a SHOOT_LEFT
```

### 完整游戏流程示例

```bash
# 1. 创建游戏
/>catamaze new
✓ Game created: abc123-...
HP: ♥♥♥♥♥  Ammo: ●●●
...

# 2. 添加几个动作
/>catamaze a MOVE_UP
✓ Action queued (1 in queue)

/>catamaze a SHOOT_RIGHT
✓ Action queued (2 in queue)

# 3. 执行tick
/>catamaze t
✓ Tick executed
...

# 4. 查看状态
/>catamaze o
HP: ♥♥♥♥♥  Ammo: ●●
Alive: true
...
```

## 🎯 动作类型

### 移动
- `MOVE_UP` - 向上
- `MOVE_DOWN` - 向下
- `MOVE_LEFT` - 向左
- `MOVE_RIGHT` - 向右

### 射击
- `SHOOT_UP` - 向上射击
- `SHOOT_DOWN` - 向下射击
- `SHOOT_LEFT` - 向左射击
- `SHOOT_RIGHT` - 向右射击

### 其他
- `WAIT` - 等待

## 🐛 故障排除

### 问题1: `'catamaze' is not recognized`

**原因**: 命令尚未注册或构建未完成

**解决**:
```bash
cd ~/Desktop/catachess
npm run build
# 然后刷新浏览器
```

### 问题2: 命令注册但无响应

**原因**: API连接失败

**检查**:
```bash
# 测试API是否可访问
curl https://catamaze.catachess.com/health

# 应该返回:
{"status":"healthy","service":"catamaze-api","version":"0.1.0"}
```

**解决**: 检查网络连接或API URL配置

### 问题3: TypeScript 错误

**原因**: 类型定义不匹配

**解决**:
```bash
cd ~/Desktop/catachess
npm run type-check
# 查看错误详情
```

如果是CataMaze模块的类型问题：
```bash
cd ~/Desktop/catamaze/frontend/terminal
# 确保有正确的TypeScript配置
```

### 问题4: 符号链接失效

**检查**:
```bash
ls -la ~/Desktop/catachess/patch/modules/catamaze
# 应该显示: catamaze -> /Users/alex_1/Desktop/catamaze/frontend/terminal
```

**修复**:
```bash
ln -sf ~/Desktop/catamaze/frontend/terminal ~/Desktop/catachess/patch/modules/catamaze
```

## 📊 验证集成成功

### 1. 检查命令列表
在终端中输入：
```bash
help
```
应该能看到 `catamaze` 在命令列表中。

### 2. 测试帮助
```bash
catamaze help
```
应该显示CataMaze命令的帮助信息。

### 3. 创建测试游戏
```bash
catamaze new
```
应该成功创建游戏并显示初始状态。

### 4. 检查浏览器控制台
按 F12 打开浏览器开发工具，切换到 Console 标签：
- 不应该有红色错误
- 可能有一些网络请求日志

## 🎨 自定义

### 修改API URL (如果需要)

编辑 `catamaze/frontend/terminal/apiClient.ts`:
```typescript
const BASE_URL = process.env.REACT_APP_API_URL || 'https://your-custom-url.com';
```

然后：
```bash
cd ~/Desktop/catamaze
git add frontend/terminal/apiClient.ts
git commit -m "Update API URL"
git push

# CataChess会通过符号链接自动看到更改
cd ~/Desktop/catachess
npm run build
```

### 添加新命令选项

编辑 `catamaze/frontend/terminal/commands/handlers.ts` 添加新的处理函数，
然后在 `commands/catamaze.ts` 中添加新的case。

## 📚 相关文档

- **CataMaze**: https://github.com/SuperGaGaDragon/CataMaze
- **API文档**: https://catamaze.catachess.com/docs
- **集成指南**: CATACHESS_INTEGRATION.md
- **部署成功**: DEPLOYMENT_SUCCESS.md

## ✅ 检查清单

- [ ] CataChess 代码已拉取最新 (git pull)
- [ ] 已安装依赖 (npm install)
- [ ] 已重新构建 (npm run build)
- [ ] 浏览器已刷新
- [ ] 终端可以打开 (F12)
- [ ] 输入 `catamaze help` 有响应
- [ ] 成功创建测试游戏

---

**更新时间**: 2026-01-27
**CataChess Commit**: 9b041af
**CataMaze Commit**: 8a3e099
**状态**: ✅ Ready to Use
