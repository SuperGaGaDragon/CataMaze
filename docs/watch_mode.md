# CataMaze Watch Mode

## Overview
Watch Mode is a developer-only feature that provides a god's-eye view of the entire game state, including full map visibility and all entity positions.

## Usage

### API Endpoint
```
GET /game/watch?game_id=<game_id>-watch
```

### Authentication
Watch mode requires the game ID to end with `-watch` suffix.

**Example**:
```bash
# Regular game ID
game_id: "abc123-def456-ghi789"

# Watch mode access
watch_id: "abc123-def456-ghi789-watch"
```

### Request
```bash
curl "http://localhost:8000/game/watch?game_id=abc123-def456-ghi789-watch"
```

### Response (200 OK)
```json
{
  "game_id": "abc123-def456-ghi789",
  "tick": 25,
  "full_map": [
    ["#", "#", "#", ".", ".", ...],
    ["#", ".", ".", "#", ".", ...],
    ...
  ],
  "entities": [
    {
      "entity_id": "player",
      "entity_type": "player",
      "persona": null,
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
    }
  ],
  "bullets": [
    {
      "shooter_id": "agent_cautious_1",
      "position": {"x": 20, "y": 25},
      "direction": "UP",
      "spawn_tick": 24
    }
  ]
}
```

### Error Response (403 Forbidden)
```json
{
  "detail": "Watch mode requires game_id to end with '-watch'"
}
```

## Features

### Full Map View
- Complete 50x50 maze layout
- All tiles visible (no fog of war)
- Includes walls, empty spaces, start, exit, ammo

### Entity Tracking
- All players and agents
- Real-time positions
- HP and ammo status
- Alive/dead status
- Persona information

### Bullet Tracking
- All bullets in flight
- Shooter ID
- Current position
- Direction
- Spawn tick

## Use Cases

### 1. Development & Debugging
Watch mode is invaluable for:
- Testing agent behavior
- Debugging game logic
- Verifying map generation
- Monitoring entity interactions

### 2. Spectating
- Observe gameplay without participating
- Analyze strategy and tactics
- Record game sessions

### 3. Replay Analysis
- Review completed games
- Study agent decision-making
- Identify bugs or exploits

## Security

### Access Control
- **NOT** exposed to regular players
- Requires `-watch` suffix knowledge
- Should be disabled in production for public games

### Recommendations
1. **Development**: Unrestricted access
2. **Staging**: Limited to developers
3. **Production**: Disabled or require auth token

## Implementation

### Backend (routes.py)
```python
@router.get("/watch", response_model=WatchResponse)
async def watch_game(game_id: str, db: Session = Depends(get_db)):
    if not game_id.endswith("-watch"):
        raise HTTPException(
            status_code=403,
            detail="Watch mode requires game_id to end with '-watch'"
        )

    actual_game_id = game_id[:-6]  # Remove '-watch' suffix
    world = load_game(db, actual_game_id)

    # Return full game state
    return {
        "game_id": actual_game_id,
        "tick": world.tick,
        "full_map": world.map_grid,
        "entities": [...],
        "bullets": [...]
    }
```

### Data Exposure
Watch mode exposes:
- ✅ Full map
- ✅ All entity positions
- ✅ All entity stats
- ✅ All bullets
- ✅ Game tick

Watch mode does NOT expose:
- ❌ Player action queue
- ❌ Agent internal state
- ❌ Future predictions

## Example Usage

### Development Workflow
```bash
# 1. Create a game
POST /game/new
→ game_id: "abc123"

# 2. Play normally
POST /game/action {"game_id": "abc123", "action": "MOVE_UP"}
POST /game/tick {"game_id": "abc123"}

# 3. Watch in parallel
GET /game/watch?game_id=abc123-watch
→ Full map + all entities

# 4. Continue playing
POST /game/tick {"game_id": "abc123"}

# 5. Watch again
GET /game/watch?game_id=abc123-watch
→ Updated positions
```

### Testing Agent Behavior
```python
import requests

# Create game with agents
game_id = create_game()

for tick in range(100):
    # Execute tick
    execute_tick(game_id)

    # Watch full state
    response = requests.get(f"http://localhost:8000/game/watch?game_id={game_id}-watch")
    state = response.json()

    # Analyze agent positions
    for entity in state['entities']:
        if entity['entity_type'] == 'agent':
            print(f"{entity['entity_id']} at ({entity['position']['x']}, {entity['position']['y']})")
```

## Limitations
- No authentication required (suffix-based)
- Cannot control game from watch mode
- Read-only access
- No replay/time-travel features

## Future Enhancements
- [ ] Time-travel (replay previous ticks)
- [ ] Highlight specific entities
- [ ] Filter by entity type
- [ ] Authentication token
- [ ] WebSocket for real-time updates

## Troubleshooting

### 403 Forbidden
**Problem**: Forgot `-watch` suffix
**Solution**: Append `-watch` to game_id

### 404 Not Found
**Problem**: Game ID doesn't exist
**Solution**: Verify game_id is correct (without `-watch`)

### 400 Bad Request
**Problem**: Invalid game_id format
**Solution**: Check game_id is a valid UUID

---

**Status**: Implemented ✅
**Since**: Stage 2D
**Last Updated**: 2026-01-27
