"""
Minimal runnable example for Stage 1C modules.
Tests state structures, serialization, and state creation.
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine.state import EntityState, BulletState, WorldState, create_entity
from engine.state_factory import create_new_state, find_random_walkable_position
from maps.loader import load_map


def main():
    print("=== Stage 1C Module Test ===\n")

    # Test 1: Entity creation
    print("1. Testing entity creation...")
    player = create_entity("player", "player", 10, 10)
    print(f"   Player: {player.entity_id} at ({player.x}, {player.y})")
    print(f"   HP: {player.hp}, Ammo: {player.ammo}")
    print(f"   Alive: {player.alive}, Won: {player.won}")

    agent = create_entity("agent_aggressive_1", "agent", 20, 20, "aggressive")
    print(f"   Agent: {agent.entity_id} ({agent.persona}) at ({agent.x}, {agent.y})")
    print()

    # Test 2: Entity serialization
    print("2. Testing entity serialization...")
    player_dict = player.to_dict()
    print(f"   Serialized keys: {list(player_dict.keys())}")

    player_restored = EntityState.from_dict(player_dict)
    print(f"   Restored player: {player_restored.entity_id} at ({player_restored.x}, {player_restored.y})")
    print(f"   Match: {player.entity_id == player_restored.entity_id}")
    print()

    # Test 3: Bullet state
    print("3. Testing bullet state...")
    bullet = BulletState("player", 15, 15, "RIGHT", 5)
    print(f"   Bullet from {bullet.shooter_id} at ({bullet.x}, {bullet.y})")
    print(f"   Direction: {bullet.direction}, Spawn tick: {bullet.spawn_tick}")

    bullet_dict = bullet.to_dict()
    bullet_restored = BulletState.from_dict(bullet_dict)
    print(f"   Serialization match: {bullet.shooter_id == bullet_restored.shooter_id}")
    print()

    # Test 4: Random position finding
    print("4. Testing random walkable position...")
    grid = load_map("map1.txt")
    exclude = [(0, 0), (1, 1)]
    pos = find_random_walkable_position(grid, exclude)
    print(f"   Found position: {pos}")
    print(f"   Not in exclude list: {pos not in exclude}")
    print()

    # Test 5: Create new world state
    print("5. Testing create_new_state...")
    world = create_new_state()
    print(f"   Game ID: {world.game_id}")
    print(f"   Tick: {world.tick}")
    print(f"   Map size: {len(world.map_grid)}x{len(world.map_grid[0])}")
    print(f"   Start: ({world.start_x}, {world.start_y})")
    print(f"   Exit: ({world.exit_x}, {world.exit_y})")
    print(f"   Entities: {list(world.entities.keys())}")
    print(f"   Bullets: {len(world.bullets)}")
    print(f"   Game over: {world.game_over}")
    print()

    # Test 6: WorldState serialization
    print("6. Testing world state serialization...")
    world_dict = world.to_dict()
    print(f"   Serialized world keys: {list(world_dict.keys())}")

    world_restored = WorldState.from_dict(world_dict)
    print(f"   Restored game ID: {world_restored.game_id}")
    print(f"   Restored tick: {world_restored.tick}")
    print(f"   Entities match: {set(world.entities.keys()) == set(world_restored.entities.keys())}")
    print()

    # Test 7: JSON serialization
    print("7. Testing JSON serialization...")
    try:
        json_str = json.dumps(world_dict, indent=2)
        print(f"   JSON size: {len(json_str)} characters")
        print(f"   Can serialize to JSON: ✓")

        world_from_json = WorldState.from_dict(json.loads(json_str))
        print(f"   Can deserialize from JSON: ✓")
        print(f"   Game ID match: {world.game_id == world_from_json.game_id}")
    except Exception as e:
        print(f"   JSON serialization failed: {e}")
    print()

    print("=== All tests passed! ===")


if __name__ == "__main__":
    main()
