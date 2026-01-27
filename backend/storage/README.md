# Storage Module

Database storage for CataMaze game.

## Database Tables

### `games`
Stores game state (world state as JSON).

| Column | Type | Description |
|--------|------|-------------|
| game_id | String(36) | Primary key, UUID |
| tick | Integer | Current game tick |
| world_state | Text | JSON serialized WorldState |
| game_over | Boolean | Game over flag |
| winner_id | String(50) | Winner entity ID |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

### `logs`
Stores game events and agent logs.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key, auto-increment |
| game_id | String(36) | Reference to game |
| tick | Integer | Game tick when event occurred |
| entity_id | String(50) | Entity involved (optional) |
| event_type | String(50) | Event category |
| message | Text | Event description |
| extra_data | Text | Additional data as JSON (optional) |
| created_at | DateTime | Creation timestamp |

## Running Migrations

### Method 1: Run migration script

```bash
cd backend
export DATABASE_URL="postgresql://user:password@host:port/database"
python3 storage/migrate.py
```

### Method 2: Automatic on app startup

The database tables will be automatically created when the FastAPI app starts if they don't exist.

```python
from storage.db import init_db

# In your app startup
@app.on_event("startup")
async def startup_event():
    init_db()
```

## Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
DATABASE_URL=postgresql://user:password@host:port/database
```

Or set the environment variable before running:

```bash
export DATABASE_URL="postgresql://user:password@host:port/database"
```

## Testing Connection

```python
from storage.db import test_connection

if test_connection():
    print("Database connected!")
```

## Usage Example

```python
from storage.db import get_db
from storage.models import Game
from sqlalchemy.orm import Session

def save_game(db: Session, game_id: str, world_state_json: str):
    game = Game(
        game_id=game_id,
        tick=0,
        world_state=world_state_json,
        game_over=False
    )
    db.add(game)
    db.commit()
    db.refresh(game)
    return game
```
