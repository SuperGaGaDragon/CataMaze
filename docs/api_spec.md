# CataMaze API Specification

## Base URL
```
http://localhost:8000
```

## Endpoints

### POST /game/new
Creates a new game instance with random player and agent placement.

**Request**
```json
{}
```

**Response** (201 Created)
```json
{
  "game_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "observation": {
    "entity_id": "player",
    "hp": 5,
    "ammo": 3,
    "time": 0,
    "position": {
      "x": 10,
      "y": 15
    },
    "vision": [
      ["#", "#", ".", ".", "."],
      ["#", ".", ".", "#", "."],
      [".", ".", "@", ".", "."],
      [".", "#", ".", ".", "#"],
      [".", ".", ".", ".", "#"]
    ],
    "last_sound": null,
    "alive": true,
    "won": false,
    "game_over": false
  },
  "queue_size": 0
}
```

**Notes**:
- Player placed at random walkable position
- 3 agents placed at random walkable positions
- Start (S) and exit (E) positions loaded from map
- Returns initial observation for player

---

### POST /game/action
Queues an action for the player. Does NOT advance the game tick.

**Request**
```json
{
  "game_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "action": "MOVE_UP"
}
```

**Action values**:
- `MOVE_UP`, `MOVE_DOWN`, `MOVE_LEFT`, `MOVE_RIGHT`
- `SHOOT_UP`, `SHOOT_DOWN`, `SHOOT_LEFT`, `SHOOT_RIGHT`
- `WAIT`

**Response** (200 OK)
```json
{
  "success": true,
  "queue_size": 3,
  "message": "Action queued"
}
```

**Error Response** (400 Bad Request)
```json
{
  "success": false,
  "error": "Invalid action"
}
```

**Error Response** (404 Not Found)
```json
{
  "success": false,
  "error": "Game not found"
}
```

---

### POST /game/tick
Advances the game by one tick. Executes one action from each entity's queue.

**Request**
```json
{
  "game_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

**Response** (200 OK)
```json
{
  "tick": 1,
  "observation": {
    "entity_id": "player",
    "hp": 4,
    "ammo": 2,
    "time": 1,
    "position": {
      "x": 10,
      "y": 14
    },
    "vision": [
      [".", ".", "#", ".", "."],
      ["#", "#", ".", ".", "."],
      ["#", ".", "@", ".", "."],
      [".", "#", ".", "P", "."],
      [".", ".", ".", ".", "#"]
    ],
    "last_sound": "*click*",
    "alive": true,
    "won": false,
    "game_over": false
  },
  "events": [
    "player moved UP",
    "agent_aggressive_1 shot DOWN",
    "player hit by bullet from agent_aggressive_1",
    "player HP: 5 -> 4"
  ],
  "queue_size": 2
}
```

**Notes**:
- Pops one action from each entity's queue (or WAIT if empty)
- Resolves movement, shooting, bullet travel, hits
- Recovers bullets (every 2 ticks)
- Checks win/loss conditions
- Auto-saves world state to database
- Returns updated observation and event log

---

### POST /game/clear_queue
Clears the player's action queue (ESC key behavior).

**Request**
```json
{
  "game_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

**Response** (200 OK)
```json
{
  "success": true,
  "message": "Queue cleared"
}
```

---

### POST /game/resume
Resumes a previously saved game from the database.

**Request**
```json
{
  "game_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

**Response** (200 OK)
```json
{
  "game_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "observation": {
    "entity_id": "player",
    "hp": 3,
    "ammo": 2,
    "time": 145,
    "position": {
      "x": 25,
      "y": 30
    },
    "vision": [...],
    "last_sound": null,
    "alive": true,
    "won": false,
    "game_over": false
  },
  "queue_size": 1
}
```

**Error Response** (404 Not Found)
```json
{
  "success": false,
  "error": "Game not found"
}
```

---

### GET /game/observe
Gets the current observation for the player without advancing tick.

**Query Parameters**:
- `game_id` (required): Game UUID

**Example**:
```
GET /game/observe?game_id=a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

**Response** (200 OK)
```json
{
  "observation": {
    "entity_id": "player",
    "hp": 4,
    "ammo": 3,
    "time": 12,
    "position": {
      "x": 15,
      "y": 20
    },
    "vision": [...],
    "last_sound": null,
    "alive": true,
    "won": false,
    "game_over": false
  }
}
```

---

### GET /game/watch
**[Developer-only feature]** Provides full map view for spectating. Requires game_id to end with `-watch`.

**Query Parameters**:
- `game_id` (required): Game UUID with `-watch` suffix

**Example**:
```
GET /game/watch?game_id=a1b2c3d4-e5f6-7890-abcd-ef1234567890-watch
```

**Response** (200 OK)
```json
{
  "game_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "tick": 25,
  "full_map": [
    ["#", "#", "#", ...],
    ...
  ],
  "entities": [
    {
      "entity_id": "player",
      "entity_type": "player",
      "position": {"x": 15, "y": 20},
      "hp": 4,
      "ammo": 3,
      "alive": true,
      "won": false
    },
    {
      "entity_id": "agent_aggressive_1",
      "entity_type": "agent",
      "persona": "aggressive",
      "position": {"x": 30, "y": 35},
      "hp": 2,
      "ammo": 1,
      "alive": true,
      "won": false
    },
    ...
  ],
  "bullets_in_flight": [
    {
      "shooter_id": "agent_cautious_1",
      "position": {"x": 20, "y": 25},
      "direction": "UP",
      "spawn_tick": 24
    }
  ]
}
```

**Authorization**:
- game_id must end with `-watch` suffix
- The actual game_id is extracted by removing `-watch`
- This is a hidden developer feature, not exposed to regular players

**Error Response** (403 Forbidden)
```json
{
  "success": false,
  "error": "Watch mode requires game_id to end with '-watch'"
}
```

---

## Concurrency Limit

The server maintains a maximum of **50 concurrent games**. If this limit is reached:

**Response** (503 Service Unavailable)
```json
{
  "success": false,
  "error": "Server at capacity (50 concurrent games). Try again later."
}
```

---

## Error Handling

### Standard Error Response
```json
{
  "success": false,
  "error": "Error message describing what went wrong"
}
```

### HTTP Status Codes
- `200 OK`: Successful operation
- `201 Created`: New game created
- `400 Bad Request`: Invalid input
- `403 Forbidden`: Permission denied (e.g., watch mode without -watch suffix)
- `404 Not Found`: Game not found
- `503 Service Unavailable`: Server at capacity
