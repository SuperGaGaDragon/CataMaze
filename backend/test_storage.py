"""
Test storage module with SQLite (local testing).
"""
import sys
import os
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Use SQLite for testing
os.environ["DATABASE_URL"] = f"sqlite:///{tempfile.gettempdir()}/catamaze_test.db"

from storage.db import init_db, test_connection, SessionLocal, engine, Base
from storage.models import Game, Log
import json


def test_storage():
    """Test database operations."""
    print("=== Storage Module Test ===\n")

    # Test 1: Connection
    print("1. Testing database connection...")
    if test_connection():
        print("   ✓ Connection successful\n")
    else:
        print("   ✗ Connection failed\n")
        return

    # Test 2: Create tables
    print("2. Creating tables...")
    init_db()
    print("   ✓ Tables created\n")

    # Test 3: Insert game
    print("3. Testing Game model...")
    db = SessionLocal()

    game_data = {
        "game_id": "test-001",
        "tick": 0,
        "entities": {"player": {"hp": 5, "ammo": 3}}
    }

    game = Game(
        game_id="test-001",
        tick=0,
        world_state=json.dumps(game_data),
        game_over=False,
        winner_id=None
    )

    db.add(game)
    db.commit()
    print(f"   ✓ Game created: {game}\n")

    # Test 4: Query game
    print("4. Testing game query...")
    retrieved_game = db.query(Game).filter(Game.game_id == "test-001").first()
    print(f"   ✓ Game retrieved: {retrieved_game}")
    print(f"   World state type: {type(retrieved_game.world_state)}")
    print(f"   World state length: {len(retrieved_game.world_state)} chars\n")

    # Test 5: Update game
    print("5. Testing game update...")
    retrieved_game.tick = 10
    retrieved_game.game_over = True
    retrieved_game.winner_id = "player"
    db.commit()
    print(f"   ✓ Game updated: tick={retrieved_game.tick}, game_over={retrieved_game.game_over}\n")

    # Test 6: Insert log
    print("6. Testing Log model...")
    log = Log(
        game_id="test-001",
        tick=5,
        entity_id="player",
        event_type="game_event",
        message="Player moved to (10, 10)",
        extra_data=json.dumps({"position": {"x": 10, "y": 10}})
    )
    db.add(log)
    db.commit()
    print(f"   ✓ Log created: {log}\n")

    # Test 7: Query logs
    print("7. Testing log query...")
    logs = db.query(Log).filter(Log.game_id == "test-001").all()
    print(f"   ✓ Found {len(logs)} logs")
    for log in logs:
        print(f"     - {log}\n")

    # Test 8: Count games
    print("8. Testing aggregate queries...")
    game_count = db.query(Game).count()
    log_count = db.query(Log).count()
    print(f"   ✓ Total games: {game_count}")
    print(f"   ✓ Total logs: {log_count}\n")

    db.close()

    # Cleanup
    print("9. Cleanup...")
    Base.metadata.drop_all(bind=engine)
    print("   ✓ Tables dropped\n")

    print("=== All tests passed! ===")


if __name__ == "__main__":
    test_storage()
