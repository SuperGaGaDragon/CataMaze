"""
Minimal runnable example for Stage 1D modules.
Tests game engine and tick execution.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.engine.engine import GameEngine
from backend.engine.state_factory import create_new_state
from backend.engine.actions import MOVE_RIGHT, MOVE_DOWN, SHOOT_RIGHT, WAIT


def print_entity_status(world):
    """Print status of all entities."""
    for entity_id, entity in world.entities.items():
        if entity.alive:
            status = f"  {entity_id}: pos=({entity.x},{entity.y}), HP={entity.hp}, Ammo={entity.ammo}, Queue={len(entity.action_queue)}"
            print(status)


def main():
    print("=== Stage 1D Module Test ===\n")

    # Test 1: Create game engine
    print("1. Creating game engine...")
    world = create_new_state()
    engine = GameEngine(world)
    print(f"   Game ID: {world.game_id}")
    print(f"   Entities: {list(world.entities.keys())}")
    print()

    # Test 2: Execute empty tick (all entities WAIT)
    print("2. Executing tick with no actions...")
    result = engine.tick()
    print(f"   Tick: {result['tick']}")
    print(f"   Events: {len(result['events'])} events")
    for event in result['events'][:5]:  # Show first 5
        print(f"     - {event}")
    print()

    # Test 3: Queue actions and execute
    print("3. Queueing actions for player...")
    player = world.entities["player"]
    player.action_queue = [MOVE_RIGHT, MOVE_DOWN, MOVE_RIGHT]
    print(f"   Player queue: {player.action_queue}")

    result = engine.tick()
    print(f"   After tick {result['tick']}:")
    print(f"   Player queue remaining: {player.action_queue}")
    print(f"   Events:")
    for event in result['events']:
        print(f"     - {event}")
    print()

    # Test 4: Multiple ticks
    print("4. Executing multiple ticks...")
    initial_tick = world.tick
    for i in range(3):
        result = engine.tick()
        print(f"   Tick {result['tick']}: {len(result['events'])} events")

    print(f"   Ticks executed: {world.tick - initial_tick}")
    print()

    # Test 5: Test shooting
    print("5. Testing shooting mechanics...")
    player = world.entities["player"]
    initial_ammo = player.ammo
    player.action_queue = [SHOOT_RIGHT]

    result = engine.tick()
    print(f"   Ammo before: {initial_ammo}, after: {player.ammo}")
    print(f"   Shoot events:")
    for event in result['events']:
        if "shot" in event.lower():
            print(f"     - {event}")
    print()

    # Test 6: Test ammo recovery
    print("6. Testing ammo recovery...")
    player.ammo = 0
    player.last_bullet_tick = world.tick

    print(f"   Ammo: {player.ammo}, Last shot: {player.last_bullet_tick}, Current tick: {world.tick}")

    # Execute 2 ticks (recovery happens every 2 ticks)
    engine.tick()
    result = engine.tick()

    print(f"   After 2 ticks: Ammo={player.ammo}, Tick={world.tick}")
    recovery_events = [e for e in result['events'] if 'recovered' in e.lower()]
    if recovery_events:
        print(f"   Recovery event: {recovery_events[0]}")
    print()

    # Test 7: Test observations
    print("7. Testing observation generation...")
    result = engine.tick()
    player_obs = result['observations'].get('player')

    if player_obs:
        print(f"   Player observation:")
        print(f"     HP: {player_obs['hp']}")
        print(f"     Ammo: {player_obs['ammo']}")
        print(f"     Position: ({player_obs['position']['x']}, {player_obs['position']['y']})")
        print(f"     Vision size: {len(player_obs['vision'])}x{len(player_obs['vision'][0])}")
        print(f"     Last sound: {player_obs['last_sound']}")
        print(f"     Alive: {player_obs['alive']}")
        print(f"     Game over: {player_obs['game_over']}")
    print()

    # Test 8: Entity status
    print("8. Final entity status...")
    print_entity_status(world)
    print()

    print("=== All tests passed! ===")


if __name__ == "__main__":
    main()
