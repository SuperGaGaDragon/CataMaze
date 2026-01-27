"""
Minimal runnable example for Stage 1A modules.
Tests map loading, actions, position calculations, and local vision.
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.maps.loader import load_map, get_start_and_exit
from backend.engine.actions import (
    MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT,
    SHOOT_UP, SHOOT_LEFT, get_direction_vector, is_valid_action
)
from backend.engine.position import (
    add_vector, is_in_bounds, is_walkable,
    can_move_to, get_next_position, manhattan_distance, is_in_range
)
from backend.engine.local_map import extract_local_vision, get_vision_for_entity


def print_vision(vision):
    """Pretty print a vision grid."""
    for row in vision:
        print(''.join(row))
    print()


def main():
    print("=== Stage 1A Module Test ===\n")

    # Test 1: Load map
    print("1. Testing map loader...")
    grid = load_map("map1.txt")
    print(f"   Loaded map: {len(grid)}x{len(grid[0])}")

    start_pos, exit_pos = get_start_and_exit(grid)
    print(f"   Start position: {start_pos}")
    print(f"   Exit position: {exit_pos}")
    print()

    # Test 2: Actions
    print("2. Testing actions...")
    print(f"   MOVE_UP is valid: {is_valid_action(MOVE_UP)}")
    print(f"   Direction vector for MOVE_UP: {get_direction_vector(MOVE_UP)}")
    print(f"   Direction vector for SHOOT_LEFT: {get_direction_vector(SHOOT_LEFT)}")
    print()

    # Test 3: Position calculations
    print("3. Testing position calculations...")
    test_pos = (5, 5)
    print(f"   Test position: {test_pos}")
    print(f"   Is in bounds: {is_in_bounds(test_pos)}")
    print(f"   Is walkable: {is_walkable(grid, test_pos)}")

    # Try moving up from (5, 5)
    move_vector = get_direction_vector(MOVE_UP)
    next_pos = get_next_position(grid, test_pos, move_vector)
    print(f"   After MOVE_UP: {next_pos}")

    # Test wall collision
    wall_test = (0, 0)  # This is '#'
    print(f"   Position {wall_test} is walkable: {is_walkable(grid, wall_test)}")
    print()

    # Test 4: Distance calculations
    print("4. Testing distance calculations...")
    pos1 = (10, 10)
    pos2 = (15, 12)
    print(f"   Manhattan distance {pos1} -> {pos2}: {manhattan_distance(pos1, pos2)}")
    print(f"   In range (3): {is_in_range(pos1, pos2, 3)}")
    print()

    # Test 5: Local vision
    print("5. Testing local vision extraction...")
    center = (10, 10)
    vision = extract_local_vision(grid, center, 5)
    print(f"   5x5 vision centered at {center}:")
    print_vision(vision)

    # Test 6: Vision with entities
    print("6. Testing vision with entities...")
    entities = {
        "player": (10, 10),
        "agent1": (12, 10),
        "agent2": (10, 8)
    }
    rendered_vision = get_vision_for_entity(grid, (10, 10), entities, "player", 5)
    print("   Vision for player (@ = self, P = others):")
    print_vision(rendered_vision)

    print("=== All tests passed! ===")


if __name__ == "__main__":
    main()
