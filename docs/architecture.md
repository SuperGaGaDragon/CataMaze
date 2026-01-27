# CataMaze Architecture

## Module Overview

### Backend

#### `backend/main.py`
FastAPI application entry point. Registers routes and starts the server.

#### `backend/engine/`
Core game logic and world state management.
- **position.py**: Player/agent position calculations and movement validation
- **hp.py**: HP tracking and death determination
- **bullet.py**: Bullet recovery (every 2 seconds) and hit detection
- **actions.py**: Action definitions (MOVE_UP/DOWN/LEFT/RIGHT, SHOOT_UP/DOWN/LEFT/RIGHT, WAIT)
- **local_map.py**: Extract 5x5 vision from the global 50x50 map
- **engine.py**: Main engine orchestrating world state, tick progression, and saving

#### `backend/maps/`
Map data and loading.
- **maze1.txt**: 50x50 map file (#=wall, .=path, S=start, E=exit)
- **loader.py**: Parse map file into 2D array

#### `backend/api/`
HTTP API routes and models.
- **routes.py**: API endpoints
  - POST /game/new
  - POST /game/action
  - POST /game/tick
  - POST /game/clear_queue
  - POST /game/resume
  - GET /game/observe
  - GET /game/watch
- **models.py**: Pydantic request/response models

#### `backend/storage/`
Database persistence layer.
- **games_store.py**: Save/load game state to PostgreSQL
- **log_store.py**: Store agent reward/penalty logs

#### `backend/agents/`
Agent system (human proxy + RL agents).
- **human.py**: Human player input queue proxy
- **base.py**: Base agent interface
- **registry.py**: Agent registry (engine queries this for all agents)
- **personas.py**: PersonaConfig data structure
- **personas/**: JSON configs for aggressive/cautious/explorer
- **log/**: Directory for reward/penalty logs
- **rl/**: RL agent implementation
  - **agent.py**: RLAgent entry point (engine calls `.act(obs)`)
  - **encoder.py**: Convert observation to numeric state vector
  - **policy.py**: Shared policy network for all agents
  - **reward.py**: Reward calculation logic
  - **action_mask.py**: Personality-based action weighting

### Frontend

#### `frontend/terminal/`
Terminal UI version integrated with desktop/catachess/patch/modules/terminal.
ASCII art rendering, keyboard input (WASD + IJKL).

#### `frontend/UI/`
Static HTML/CSS/JS web UI version.
- **index.html**: Main page structure
- **style.css**: Styling for 5x5 grid and HUD
- **main.js**: Game logic and API communication
- **assets/**: Images for user/agents
  - user.png
  - aggressive.png
  - cautious.png
  - explorer.png

## Data Flow

1. User sends action via frontend (terminal or UI)
2. POST /game/action queues the action
3. POST /game/tick executes one action from queue
4. Engine updates world state, resolves combat, recovers bullets
5. State saved to PostgreSQL
6. GET /game/observe returns updated observation
7. Frontend renders new state

## Key Constraints

- Max 50 concurrent games
- Each tick = 1 second
- Each file ≤ 200 lines
- Auto-save after every tick
- Agents share policy network but calculate independent rewards
