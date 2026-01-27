# Cloudflare Pages 部署指南

## 📦 前端版本总结

### ✅ 版本1: Web UI（独立前端）
**位置**: `frontend/UI/`
**用途**: 独立的Web界面，可部署到Cloudflare Pages
**API**: https://catamaze.catachess.com ✅ 已配置
**文件**:
- `index.html` - 主页面
- `main.js` - 主逻辑（ES6模块）
- `ui.js` - UI更新逻辑
- `api.js` - API客户端 ✅ 已更新为生产URL
- `style.css`, `layout.css`, `controls.css`, `game-area.css` - 样式
- `assets/` - 资源文件

### ✅ 版本2: 伪终端版本（CataChess集成）
**位置**: `frontend/terminal/`
**用途**: 集成到CataChess的伪终端命令
**API**: https://catamaze.catachess.com ✅ 已配置
**集成**: 已通过符号链接集成到CataChess

---

## 🚀 Cloudflare Pages 部署步骤

### 方法1: 通过 Cloudflare Dashboard（推荐）

#### 1. 连接GitHub仓库

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. 选择你的账户
3. 点击左侧菜单 **Pages**
4. 点击 **Create a project**
5. 点击 **Connect to Git**
6. 选择 **GitHub**，授权Cloudflare访问
7. 选择仓库: `SuperGaGaDragon/CataMaze`

#### 2. 配置构建设置

```
Project name: catamaze-game
Production branch: main
Build command: (留空 - 静态文件)
Build output directory: frontend/UI
Root directory: /
```

#### 3. 高级设置

**环境变量**: 不需要

**Build settings**:
- Framework preset: `None`
- Build command: (留空)
- Build output directory: `frontend/UI`

#### 4. 部署

点击 **Save and Deploy**

Cloudflare会自动：
- 克隆仓库
- 部署 `frontend/UI` 目录
- 生成URL（例如：`catamaze-game.pages.dev`）

#### 5. 自定义域名（可选）

如果你想使用自定义域名：
1. 进入 Pages 项目设置
2. 点击 **Custom domains**
3. 添加域名（例如：`game.catachess.com`）
4. 按照提示配置DNS

---

### 方法2: 通过 Wrangler CLI

#### 1. 安装 Wrangler

```bash
npm install -g wrangler
```

#### 2. 登录 Cloudflare

```bash
wrangler login
```

#### 3. 部署

```bash
cd ~/Desktop/catamaze

# 部署frontend/UI目录
wrangler pages deploy frontend/UI --project-name=catamaze-game
```

---

## 📝 部署后配置

### 检查清单

- [ ] 部署成功
- [ ] 访问Cloudflare提供的URL
- [ ] 测试"New Game"按钮
- [ ] 验证API连接（检查浏览器Console）
- [ ] 测试移动和射击
- [ ] 验证游戏逻辑

### 验证部署

**1. 访问URL**
```
https://catamaze-game.pages.dev
或
https://your-custom-domain.com
```

**2. 打开浏览器开发工具**
- 按F12
- 切换到Network标签
- 点击"New Game"
- 应该看到对 `https://catamaze.catachess.com/game/new` 的请求

**3. 检查Console**
- 不应该有CORS错误
- 不应该有404错误

---

## 🔧 CORS配置

如果遇到CORS问题，需要在Railway后端配置：

编辑 `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://catamaze-game.pages.dev",
        "https://your-custom-domain.com",
        "*"  # 或保持通配符
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

当前配置已经是 `allow_origins=["*"]`，所以应该没问题。

---

## 📊 目录结构（Cloudflare部署）

```
frontend/UI/  (部署根目录)
├── index.html          # 入口文件
├── main.js             # 主逻辑
├── ui.js               # UI控制
├── api.js              # API客户端 ✅
├── style.css           # 主样式
├── layout.css          # 布局
├── controls.css        # 控件样式
├── game-area.css       # 游戏区域样式
└── assets/             # 静态资源
    └── (图片、图标等)
```

---

## 🎮 功能特性

**已实现**:
- ✅ 创建新游戏
- ✅ 移动控制（WASD键 + 按钮）
- ✅ 射击控制（IJKL键 + 按钮）
- ✅ 5x5视野显示
- ✅ HP/弹药显示
- ✅ 事件日志
- ✅ 队列管理
- ✅ 游戏结束模态框
- ✅ 键盘快捷键

**键盘控制**:
- `W/A/S/D` - 移动
- `I/J/K/L` - 射击
- `Space` - 等待
- `ESC` - 清空队列

---

## 🐛 故障排除

### 问题1: 部署失败

**检查**:
- 确认 `frontend/UI/` 目录存在
- 确认 `index.html` 存在
- 检查Cloudflare构建日志

### 问题2: 页面空白

**检查**:
- 打开浏览器Console查看错误
- 验证所有CSS和JS文件路径正确
- 检查是否有ES6模块错误

### 问题3: API连接失败

**症状**: 点击"New Game"无响应

**检查**:
1. 浏览器Console是否有CORS错误
2. 验证API URL: `https://catamaze.catachess.com/health`
3. 检查 `api.js` 中的 `API_BASE_URL`

**解决**:
```bash
# 测试API
curl https://catamaze.catachess.com/health

# 应该返回:
{"status":"healthy","service":"catamaze-api","version":"0.1.0"}
```

### 问题4: CORS错误

**错误信息**:
```
Access to fetch at 'https://catamaze.catachess.com/game/new' from origin
'https://catamaze-game.pages.dev' has been blocked by CORS policy
```

**解决**:
后端已配置 `allow_origins=["*"]`，应该不会有这个问题。如果还有问题，检查Railway部署日志。

---

## 🔄 自动部署

Cloudflare Pages会自动监听GitHub推送：

**当你推送到main分支**:
```bash
cd ~/Desktop/catamaze
git add .
git commit -m "Update UI"
git push origin main
```

**Cloudflare会自动**:
1. 检测到推送
2. 拉取最新代码
3. 重新部署
4. 更新live URL

**查看部署状态**:
- Cloudflare Dashboard > Pages > catamaze-game > Deployments

---

## 📱 移动端优化（未来）

当前UI是桌面优先设计，未来可以添加：
- [ ] 响应式布局
- [ ] 触摸控制
- [ ] 虚拟摇杆
- [ ] 移动端优化样式

---

## 🎨 自定义品牌

### 修改标题和图标

编辑 `frontend/UI/index.html`:
```html
<title>CataMaze - Your Custom Title</title>
<link rel="icon" href="assets/favicon.ico">
```

### 修改样式

编辑CSS文件自定义：
- `style.css` - 全局样式
- `layout.css` - 布局
- `controls.css` - 按钮和控件
- `game-area.css` - 游戏区域

---

## 📈 性能优化

### 已优化
- ✅ 纯静态HTML/CSS/JS
- ✅ ES6模块（浏览器原生支持）
- ✅ 无构建步骤（快速部署）

### 未来优化
- [ ] 图片压缩
- [ ] CSS/JS压缩
- [ ] CDN缓存配置
- [ ] Service Worker（离线支持）

---

## 📚 相关链接

- **Cloudflare Pages文档**: https://developers.cloudflare.com/pages/
- **Wrangler文档**: https://developers.cloudflare.com/workers/wrangler/
- **CataMaze API**: https://catamaze.catachess.com/docs
- **GitHub仓库**: https://github.com/SuperGaGaDragon/CataMaze

---

## ✅ 总结

**两个前端版本都已完成并配置好**:

1. **Web UI** (`frontend/UI/`)
   - ✅ 完整的游戏界面
   - ✅ API URL已配置为生产环境
   - ✅ 准备好部署到Cloudflare Pages

2. **伪终端** (`frontend/terminal/`)
   - ✅ 集成到CataChess
   - ✅ 命令已注册
   - ✅ API URL已配置为生产环境

**现在可以直接部署Web UI到Cloudflare Pages！**

---

**创建时间**: 2026-01-27
**提交**: 1fefada
**状态**: ✅ Ready for Deployment
