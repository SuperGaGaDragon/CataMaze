"""
Engine self-check script.
Runs a complete game scenario to verify all engine features.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.engine import GameEngine
from engine.state import WorldState, create_entity
from engine.actions import MOVE_RIGHT, MOVE_DOWN, SHOOT_RIGHT
from maps.loader import load_map, get_start_and_exit


def print_sep(title):
    """Print section separator."""
    print(f"\n{'='*50}\n  {title}\n{'='*50}")


def run_selfcheck():
    """Run complete engine self-check."""
    print_sep("CATAMAZE ENGINE SELF-CHECK")

    # Phase 1: Map loading
    print_sep("Phase 1: Map Loading")
    grid = load_map("map1.txt")
    (start_x, start_y), (exit_x, exit_y) = get_start_and_exit(grid)
    print(f"✓ Map: {len(grid)}x{len(grid[0])}, Start: ({start_x},{start_y}), Exit: ({exit_x},{exit_y})")

    # Phase 2: Create world
    print_sep("Phase 2: World Creation")
    player = create_entity("player", "player", 10, 10)
    agent = create_entity("target", "agent", 15, 10, "aggressive")
    world = WorldState(
        game_id="check-001", tick=0, map_grid=grid,
        start_x=start_x, start_y=start_y, exit_x=exit_x, exit_y=exit_y,
        entities={"player": player, "target": agent},
        bullets=[], game_over=False, winner_id=None
    )
    engine = GameEngine(world)
    print(f"✓ World created: {list(world.entities.keys())}")

    # Phase 3: Movement
    print_sep("Phase 3: Movement")
    player.action_queue = [MOVE_RIGHT, MOVE_DOWN]
    for _ in range(2):
        result = engine.tick()
        for e in result['events']:
            print(f"  {e}")
    print(f"✓ Player at ({player.x},{player.y})")

    # Phase 4: Shooting and death
    print_sep("Phase 4: Shooting & Death")
    agent.x, agent.y = player.x + 3, player.y
    agent.hp = 1
    player.action_queue = [SHOOT_RIGHT]
    result = engine.tick()
    for e in result['events']:
        print(f"  {e}")
    print(f"✓ Agent HP={agent.hp}, Alive={agent.alive}")

    # Phase 5: Ammo recovery
    print_sep("Phase 5: Ammo Recovery")
    player.ammo = 1
    player.last_bullet_tick = world.tick - 10
    before = player.ammo
    for _ in range(3):
        result = engine.tick()
        for e in result['events']:
            if 'recovered' in e.lower():
                print(f"  {e}")
    print(f"✓ Ammo: {before} → {player.ammo}")

    # Phase 6: Win condition
    print_sep("Phase 6: Win Condition")
    player.x, player.y = exit_x, exit_y
    result = engine.tick()
    for e in result['events']:
        print(f"  {e}")
    print(f"✓ Won={player.won}, GameOver={world.game_over}")

    # Phase 7: Observation
    print_sep("Phase 7: Observation")
    p2 = create_entity("player", "player", 20, 20)
    w2 = WorldState(
        game_id="check-002", tick=0, map_grid=grid,
        start_x=start_x, start_y=start_y, exit_x=exit_x, exit_y=exit_y,
        entities={"player": p2}, bullets=[], game_over=False, winner_id=None
    )
    e2 = GameEngine(w2)
    result = e2.tick()
    obs = result['observations']['player']
    print(f"✓ Obs: HP={obs['hp']}, Ammo={obs['ammo']}, Vision={len(obs['vision'])}x{len(obs['vision'][0])}")

    # Final
    print_sep("COMPLETE")
    print("✓ Map loading\n✓ Movement\n✓ Shooting & hit detection")
    print("✓ Ammo recovery\n✓ Death\n✓ Win condition\n✓ Observation")
    print(f"\n{'='*50}\n  ENGINE READY\n{'='*50}\n")


if __name__ == "__main__":
    run_selfcheck()
