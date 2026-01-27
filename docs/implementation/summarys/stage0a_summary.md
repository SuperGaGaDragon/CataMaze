# Stage 0A 执行总结

## 执行时间
2026-01-27

## 任务目标
阅读与范围锁定：通读文档并提炼规则、模块清单、地图格式、数据库要求和API草案

## 完成内容

### 1. ✅ 硬性规则清单
已提炼核心规则：
- 迷宫 50x50，视野 5x5，听觉 7x7
- 回合制，每tick=1秒，队列机制，ESC清空
- HP=5（第6发死），子弹3发，每2秒恢复1发
- 3种agent（aggressive/cautious/explorer），共享模型独立reward
- 最多50局并发

### 2. ✅ 模块与文件清单
已列出完整目录结构：
- backend: main.py, engine/, maps/, api/, storage/, agents/
- frontend: terminal/, UI/
- 共计约30+个文件

### 3. ✅ 地图格式要求
- 50x50 字符矩阵
- `#`=墙, `.`=路, `S`=入口, `E`=出口
- 通过 loader.py 读取为二维数组

### 4. ✅ 数据库自动迁移要求
- DATABASE_URL 已提供（Railway PostgreSQL）
- 需要 games 表和 logs 表
- 建议使用 SQLAlchemy + create_all() 自动建表

### 5. ✅ API 列表与入参/出参草案
已整理7个API端点：
- POST /game/new - 创建游戏
- POST /game/action - 提交行动
- POST /game/tick - 推进回合
- POST /game/clear_queue - 清空队列
- POST /game/resume - 恢复游戏
- GET /game/observe - 获取观测
- GET /game/watch - 观战模式

## 遇到的问题
无问题，文档描述清晰

## 未完成项
无

## 下一步
继续执行 stage0b.md
