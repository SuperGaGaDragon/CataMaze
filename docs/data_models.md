# CataMaze Data Models

## Action Enumeration

```python
MOVE_UP = "MOVE_UP"
MOVE_DOWN = "MOVE_DOWN"
MOVE_LEFT = "MOVE_LEFT"
MOVE_RIGHT = "MOVE_RIGHT"

SHOOT_UP = "SHOOT_UP"
SHOOT_DOWN = "SHOOT_DOWN"
SHOOT_LEFT = "SHOOT_LEFT"
SHOOT_RIGHT = "SHOOT_RIGHT"

WAIT = "WAIT"
```

## Entity State

Represents a player or agent in the game.

```python
{
  "entity_id": str,           # Unique ID (e.g., "player", "agent_aggressive_1")
  "entity_type": str,         # "player" or "agent"
  "persona": str | None,      # None for player, or "aggressive"/"cautious"/"explorer"
  "position": {
    "x": int,                 # 0-49
    "y": int                  # 0-49
  },
  "hp": int,                  # 0-5 (dies at 0)
  "ammo": int,                # 0-3
  "last_bullet_tick": int,    # Tick when last bullet was fired
  "alive": bool,
  "won": bool,                # True if reached exit
  "action_queue": list[str],  # List of queued actions
  "visited_positions": set    # For explorer penalty tracking
}
```

## World State

Complete game state saved after each tick.

```python
{
  "game_id": str,             # UUID
  "tick": int,                # Current tick (starts at 0)
  "map": list[list[str]],     # 50x50 2D array ('#', '.', 'S', 'E')
  "start_position": {         # Start position (S)
    "x": int,
    "y": int
  },
  "exit_position": {          # Exit position (E)
    "x": int,
    "y": int
  },
  "entities": dict[str, EntityState],  # Key = entity_id
  "bullets_in_flight": list[  # Active bullets
    {
      "shooter_id": str,
      "position": {"x": int, "y": int},
      "direction": str,       # "UP"/"DOWN"/"LEFT"/"RIGHT"
      "spawn_tick": int
    }
  ],
  "game_over": bool,
  "winner_id": str | None     # entity_id of winner, or None
}
```

## Observation

What a player/agent sees (5x5 vision).

```python
{
  "entity_id": str,
  "hp": int,
  "ammo": int,
  "time": int,                # Current tick
  "position": {
    "x": int,
    "y": int
  },
  "vision": list[list[str]],  # 5x5 grid centered on entity
                              # Values: '#', '.', '@' (self), 'P' (other entity)
  "last_sound": str | None,   # "*click*" if shot heard in 7x7 range, else None
  "alive": bool,
  "won": bool,
  "game_over": bool
}
```

## Queue Structure and Tick Behavior

- **Queue**: FIFO list of action strings
- **Input**: When user presses key, action is appended to their entity's `action_queue`
- **Tick execution**:
  1. For each entity, pop one action from `action_queue` (or WAIT if empty)
  2. Execute all actions simultaneously
  3. Resolve bullets (check hits, update positions)
  4. Recover bullets (1 per 2 ticks, max 3)
  5. Check win/loss conditions
  6. Save world state
- **ESC**: Clears the player's `action_queue`
- **1 tick = 1 second** in game time

## HP and Ammo Rules

### HP
- **Initial**: 5
- **Max**: 5
- **Death**: HP reaches 0 (can take 5 hits, 6th hit kills)
- **Recovery**: None (no healing)

### Ammo
- **Initial**: 3
- **Max**: 3
- **Firing**: Consumes 1 ammo (cannot fire if ammo = 0)
- **Recovery**: 1 bullet every 2 ticks (if ammo < 3)
  - Example: Fire at tick 0 (ammo=2), recover at tick 2 (ammo=3)

## Win/Loss Conditions

### Win
- Player reaches exit position (E)
- `won = True`, `game_over = True`

### Loss
- Player HP reaches 0
- `alive = False`, `game_over = True`

### Agent Death
- Agent HP reaches 0
- `alive = False` for that agent
- Game continues until player wins or dies

## Bullet Mechanics

### Firing
- Consumes 1 ammo
- Creates bullet at entity's position + 1 cell in direction
- Bullet travels 1 cell per tick until:
  - Hits wall (#): disappears
  - Hits entity: deals 1 damage, disappears
  - Reaches map edge: disappears

### Hit Detection
- Bullet occupies same cell as entity
- Reduce entity HP by 1
- Remove bullet

### Sound
- Any entity within 7x7 range of a shot hears "*click*"
- Stored in `last_sound` field of observation
