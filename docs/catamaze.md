CataMaze游戏：

一些env 说明1
一些环境变量：
DATABASE_URL = postgresql://postgres:xkwJlPWNpIYfmsjaPQoRkFJtVLdsrcGW@postgres.railway.internal:5432/railway
存储都在这里，到时候自动建表

功能简介

- 终端游戏，暂时部署于desktop/catachess/patch/modules/terminal伪终端，不上真终端。
- 单机游戏。
- 巨大的迷宫（迷宫地图不变），有进口 1，出口 1，用户和agent 随机放置，出去就好。
- 每个人最多 3 发子弹，子弹每 2 秒恢复一发，上限 3 发。
- 每个人的最多忍受 5 发子弹，6 发就死。
- agent用 RL，奖惩机制，之后可能介入 LLM 。
- 视野：5x5，迷宫大小：50x50
- 页面范例：
╔══════════════════════╗
║        Cata MAZE     ║
╠══════════════════════╣
║ HP: 5     Ammo: 3
║ Time: 02:41          ║
╠══════════════════════╣
║        VISION        ║
║  #  .  .  .  .       ║
║  .  #  #  #  .       ║
║  .  #  @  .  .       ║
║  .  #  P  .  #       ║
║  .  .  .  .  #       ║
╠══════════════════════╣
║ Last sound: *click*  ║
║ Memory: corridor left│
╠══════════════════════╣
║ w/a/s/d  move        ║
║ i/j/k/l/       shoot ║
║                      ║
╚══════════════════════╝

 last sound click：如图，视线范围 5x5，最近 7x7 范围内有设计
 . : 可以走的路
 # ：墙
 @ ：我
 P：对手
 
 - 回合制，每次操作都是一秒。每回合只能做一件事：MOVE/SHOOT/WAIT
 - 一秒（一个 tick）只执行 1 个 action， 多次输入 → 进入队列，按顺序，每个 tick 取 1 个，ESC = 清空队列
 - 存储 game id 可以 resume 。如果 gameid后加上"-watch"，就进入“神的地图”观看（这个功能仅开发者知道，不对外公开）
 - 并发：最多同时进行 50 局，再多就拒绝/game/new
 - agent 共三个（RL）
 aggressive:  hit_reward更高, time_penalty更高
 cautious:    death_penalty更高, shoot_penalty更高
 explorer:    time_penalty更高, revisit_penalty更高
 
 agents 共享一个模型，但是独立算 reward 。不搞联盟之类的。

 
 
 需要的代码架构：
 
 desktop/catamaze
 
 catamaze/requirements.txt
 
 backend/main.py
 
 backend/engine
 backend/engine/position.py 玩家或 agent 位置计算
 backend/engine/hp.py 计算玩家或 agent血量,死亡判定
 backend/engine/bullet.py 子弹恢复判定&命中判定
 backend/engine/actions.py 定义MOVE_UP/DOWN/LEFT/RIGHT,SHOOT_UP/LEFT/DOWN/RIGHT
 backend/engine/local_map.py 从全局地图中裁剪 5x5 的，返回用户看的那个图
 backend/engine/engine.py 1 、保存世界状态 2 、把这个文件夹的那些串起来。
 
 backend/maps 全局真相
 backend/maps/maze1.txt
 backend/maps/loader.py 读 50x50，返回二维数组

 backend/api
 POST /game/new - 生成 game_id, 随机放置玩家，返回初始 observation
 POST /game/action - 提交一个 action。注意，action 只是意图。tick 是真实出现的推进。每一秒才出现一个 action 。如果用户一秒内输入多个 actions，全部进入队列，还是每秒执行。esc 清空队列
 POST /game/tick - 推进一个回合：执行engine.tick()，结算射击/移动/恢复。每一个 tick，都自动保存！
 POST /game/clear_queue esc之后，清空队列
 POST /game/resume - 恢复一个游戏（退出后自动保存，输入 game id 自动恢复（从数据库 load 最近一次 tick 的状态）
 GET /game/observe - 获取当前视野
 GET /game/watch - 观战，全局视野。如果game_id 后面加上“-watch" 就可以看全局
 
 backend/agents
 backend/agents/human.py 玩家输入队列代理（不让 agents 知道玩家是玩家，让 agents 把玩家也当成 agents）
 backend/agents/base.py 
 backend/agents/registry.py backend/engine从这里读配置。Engine -> registry -> Humanagent /RL agent
 backend/agents/personas.py personaconfig数据结构
 backend/personas/aggressive.json, cautious.json, explorer.json
  
 aggressive:  hit_reward更高, time_penalty更高
 cautious:    death_penalty更高, shoot_penalty更高
 explorer:    time_penalty更高, revisit_penalty更高
 
 backend/agents/log 加分扣分 log打出来
 backend/agents/rl/agent.py - agent 的入口层，engine → RLAgent.act(obs) → action 不管任何训练细节和 reward 计算
 backend/agents/rl/encoder.py - 翻译成 RL 能用的数字
 backend/agents/rl/policy.py state_vector → policy → action_scores，多个 agent 共享。
 backend/agents/rl/reward.py reward 计算环节
 backend/agents/rl/action_mask.py 人格的一些加权，比如cautious 低 hp 时候降低 shoot 概率，Explorer 提高 move 概率，等

 
 
 backend/storage/
 backend/storage/log_store.py 存储 log
 backend/storage/games_store.py 存储 games
 自动用 postgres 建表。
 

 frontend 
 这里 enable 两个 version，一个接desktop/catachess/patch/modules/terminal，一个新弄一个 ui
 
 frontend/terminal 
 这里直接接到desktop/catachess/patch/modules/terminal,你看看怎么接过去。
 这是 immersive repl，不是 shell，不要乱换行什么的。这里用户体验感和“必须是终端”的约束如果冲突，那就取前者
 
 frontend/UI
 这是 UI版本，画 5x5 方格在里面，用静态 html
 UI/index.html
 UI/style.css
 UI/main.js
 UI/assets 放用户/agent 出现的照片。用户是user.png。三个 agent 分别对应剩下三张照片
 
 墙是灰色的，当中两个"//"，白色方格就是可以走
 
 
 
 
 
 
 
 