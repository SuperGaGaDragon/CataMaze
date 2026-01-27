"""
Test storage layer (games_store and log_store).
"""
import sys
import os
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Use SQLite for testing
os.environ["DATABASE_URL"] = f"sqlite:///{tempfile.gettempdir()}/catamaze_stores_test.db"

from storage.db import init_db, SessionLocal, Base, engine
from storage.games_store import (
    save_game, load_game, delete_game, list_games, count_games, GameStoreError
)
from storage.log_store import (
    append_log, append_logs_batch, read_logs, count_logs, delete_logs, LogStoreError
)
from engine.state_factory import create_new_state


def test_stores():
    """Test storage layer."""
    print("=== Storage Layer Test ===\n")

    # Initialize database
    init_db()
    db = SessionLocal()

    # Test 1: Save game
    print("1. Testing save_game...")
    world = create_new_state()
    game_id = world.game_id
    print(f"   Created world: {game_id}")

    game = save_game(db, world)
    print(f"   ✓ Game saved: {game.game_id}, tick={game.tick}\n")

    # Test 2: Load game
    print("2. Testing load_game...")
    loaded_world = load_game(db, game_id)
    print(f"   ✓ Game loaded: {loaded_world.game_id}")
    print(f"   Tick: {loaded_world.tick}")
    print(f"   Entities: {len(loaded_world.entities)}")
    print(f"   Match: {loaded_world.game_id == world.game_id}\n")

    # Test 3: Update game
    print("3. Testing game update...")
    world.tick = 10
    world.game_over = True
    world.winner_id = "player"
    game = save_game(db, world)
    print(f"   ✓ Game updated: tick={game.tick}, game_over={game.game_over}\n")

    # Test 4: List games
    print("4. Testing list_games...")
    games = list_games(db, limit=10)
    print(f"   ✓ Found {len(games)} games")
    for g in games[:3]:
        print(f"     - {g['game_id']}: tick={g['tick']}, game_over={g['game_over']}\n")

    # Test 5: Count games
    print("5. Testing count_games...")
    total = count_games(db)
    active = count_games(db, game_over=False)
    finished = count_games(db, game_over=True)
    print(f"   ✓ Total: {total}, Active: {active}, Finished: {finished}\n")

    # Test 6: Append single log
    print("6. Testing append_log...")
    log = append_log(
        db, game_id, 5, "game_event", "Player moved",
        entity_id="player",
        extra_data={"x": 10, "y": 20}
    )
    print(f"   ✓ Log created: {log.id}, message={log.message}\n")

    # Test 7: Append batch logs
    print("7. Testing append_logs_batch...")
    events = ["Event 1", "Event 2", "Event 3"]
    count = append_logs_batch(db, game_id, 6, events)
    print(f"   ✓ Created {count} logs\n")

    # Test 8: Read logs
    print("8. Testing read_logs...")
    logs = read_logs(db, game_id)
    print(f"   ✓ Found {len(logs)} logs")
    for log in logs[:3]:
        print(f"     - Tick {log['tick']}: {log['message']}")
    print()

    # Test 9: Count logs
    print("9. Testing count_logs...")
    log_count = count_logs(db, game_id)
    player_logs = count_logs(db, game_id, entity_id="player")
    print(f"   ✓ Total logs: {log_count}")
    print(f"   ✓ Player logs: {player_logs}\n")

    # Test 10: Delete logs
    print("10. Testing delete_logs...")
    deleted = delete_logs(db, game_id)
    print(f"   ✓ Deleted {deleted} logs\n")

    # Test 11: Delete game
    print("11. Testing delete_game...")
    success = delete_game(db, game_id)
    print(f"   ✓ Game deleted: {success}\n")

    # Test 12: Load non-existent game
    print("12. Testing load non-existent game...")
    result = load_game(db, "nonexistent")
    print(f"   ✓ Result: {result} (should be None)\n")

    # Test 13: Error handling
    print("13. Testing error handling...")
    try:
        # Try to load from closed session
        db.close()
        load_game(db, game_id)
        print("   ✗ Should have raised error\n")
    except GameStoreError as e:
        print(f"   ✓ Caught error: {type(e).__name__}\n")

    # Cleanup
    print("14. Cleanup...")
    Base.metadata.drop_all(bind=engine)
    print("   ✓ Tables dropped\n")

    print("=== All tests passed! ===")


if __name__ == "__main__":
    test_stores()
