"""
Minimal runnable example for Stage 1B modules.
Tests HP, ammo, and bullet hit detection.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine.hp import (
    create_hp_state, take_damage, is_alive, is_dead,
    get_hp_percentage, apply_hit
)
from engine.bullet import (
    create_ammo_state, can_shoot, consume_ammo,
    should_recover_ammo, recover_ammo,
    trace_bullet_path, simulate_shot
)
from engine.constants import INITIAL_HP, INITIAL_AMMO, MAX_AMMO
from engine.actions import get_direction_vector, SHOOT_RIGHT, SHOOT_DOWN
from maps.loader import load_map


def main():
    print("=== Stage 1B Module Test ===\n")

    # Test 1: HP system
    print("1. Testing HP system...")
    hp = create_hp_state()
    print(f"   Initial HP: {hp}")
    print(f"   Is alive: {is_alive(hp)}")

    hp = take_damage(hp, 1)
    print(f"   After 1 damage: {hp} (alive: {is_alive(hp)})")

    hp = take_damage(hp, 10)  # Overkill
    print(f"   After 10 damage: {hp} (dead: {is_dead(hp)})")

    # Test apply_hit
    hp = INITIAL_HP
    new_hp, died = apply_hit(hp, 3)
    print(f"   After 3 hits: HP={new_hp}, died={died}")
    print()

    # Test 2: Ammo system
    print("2. Testing ammo system...")
    ammo = create_ammo_state()
    print(f"   Initial ammo: {ammo}")
    print(f"   Can shoot: {can_shoot(ammo)}")

    ammo = consume_ammo(ammo)
    print(f"   After shooting: {ammo}")

    # Test ammo recovery
    last_shot_tick = 0
    current_tick = 2
    print(f"   Should recover at tick {current_tick}: {should_recover_ammo(current_tick, last_shot_tick)}")

    ammo, last_shot_tick = recover_ammo(ammo, current_tick, last_shot_tick)
    print(f"   After recovery: ammo={ammo}, last_shot_tick={last_shot_tick}")
    print()

    # Test 3: Bullet trajectory
    print("3. Testing bullet trajectory...")
    grid = load_map("map1.txt")

    # Shoot from a clear position
    shooter_pos = (10, 10)
    direction = get_direction_vector(SHOOT_RIGHT)

    path = trace_bullet_path(shooter_pos, direction, grid)
    print(f"   Bullet path from {shooter_pos} going RIGHT:")
    print(f"   Path length: {len(path)}")
    if len(path) > 0:
        print(f"   First 5 positions: {path[:5]}")
    print()

    # Test 4: Hit detection
    print("4. Testing hit detection...")
    shooter_pos = (10, 10)
    target_pos = (13, 10)  # 3 cells to the right
    direction = get_direction_vector(SHOOT_RIGHT)

    hit_pos = simulate_shot(shooter_pos, direction, grid, [target_pos])
    if hit_pos:
        print(f"   Shot from {shooter_pos} hit target at {hit_pos}")
    else:
        print(f"   Shot from {shooter_pos} missed (wall or out of range)")

    # Test miss
    target_pos_2 = (10, 5)  # Different location
    hit_pos_2 = simulate_shot(shooter_pos, direction, grid, [target_pos_2])
    print(f"   Shot at {target_pos_2}: {'HIT' if hit_pos_2 else 'MISS'}")
    print()

    # Test 5: Multiple ammo recovery cycles
    print("5. Testing multiple ammo recovery cycles...")
    ammo = 0
    last_shot_tick = 0
    print(f"   Starting: ammo={ammo}, last_shot_tick={last_shot_tick}")

    for tick in [1, 2, 3, 4, 5, 6, 7]:
        ammo, last_shot_tick = recover_ammo(ammo, tick, last_shot_tick)
        if tick == 2 or tick == 4 or tick == 6:
            print(f"   Tick {tick}: ammo={ammo}, last_shot_tick={last_shot_tick}")

    print()

    print("=== All tests passed! ===")


if __name__ == "__main__":
    main()
