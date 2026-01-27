"""
Position calculations and movement validation.
"""
from typing import Tuple, List


def add_vector(pos: Tuple[int, int], vector: Tuple[int, int]) -> Tuple[int, int]:
    """
    Add a direction vector to a position.

    Args:
        pos: (x, y) current position
        vector: (dx, dy) direction vector

    Returns:
        (new_x, new_y) new position
    """
    return (pos[0] + vector[0], pos[1] + vector[1])


def is_in_bounds(pos: Tuple[int, int], width: int = 50, height: int = 50) -> bool:
    """
    Check if position is within map bounds.

    Args:
        pos: (x, y) position
        width: Map width (default 50)
        height: Map height (default 50)

    Returns:
        True if in bounds, False otherwise
    """
    x, y = pos
    return 0 <= x < width and 0 <= y < height


def is_walkable(grid: List[List[str]], pos: Tuple[int, int]) -> bool:
    """
    Check if a position is walkable (not a wall).

    Args:
        grid: 2D map array
        pos: (x, y) position to check

    Returns:
        True if walkable (not '#'), False if wall or out of bounds
    """
    if not is_in_bounds(pos, len(grid[0]), len(grid)):
        return False

    x, y = pos
    cell = grid[y][x]
    return cell != '#'


def can_move_to(grid: List[List[str]], pos: Tuple[int, int]) -> bool:
    """
    Check if entity can move to a position.

    Args:
        grid: 2D map array
        pos: (x, y) target position

    Returns:
        True if can move (in bounds and walkable), False otherwise
    """
    return is_in_bounds(pos, len(grid[0]), len(grid)) and is_walkable(grid, pos)


def get_next_position(
    grid: List[List[str]],
    current_pos: Tuple[int, int],
    direction_vector: Tuple[int, int]
) -> Tuple[int, int]:
    """
    Calculate next position after moving in a direction.
    If the target is blocked, returns current position (no movement).

    Args:
        grid: 2D map array
        current_pos: (x, y) current position
        direction_vector: (dx, dy) direction to move

    Returns:
        (x, y) new position (or current position if blocked)
    """
    target_pos = add_vector(current_pos, direction_vector)

    if can_move_to(grid, target_pos):
        return target_pos
    else:
        # Blocked, stay in current position
        return current_pos


def manhattan_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
    """
    Calculate Manhattan distance between two positions.

    Args:
        pos1: (x, y) first position
        pos2: (x, y) second position

    Returns:
        Manhattan distance
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def is_in_range(pos1: Tuple[int, int], pos2: Tuple[int, int], range_size: int) -> bool:
    """
    Check if two positions are within a certain range (Chebyshev distance).
    Used for sound detection (7x7 means max 3 cells away in any direction).

    Args:
        pos1: (x, y) first position
        pos2: (x, y) second position
        range_size: Max distance (e.g., 3 for 7x7 grid)

    Returns:
        True if within range, False otherwise
    """
    dx = abs(pos1[0] - pos2[0])
    dy = abs(pos1[1] - pos2[1])
    return max(dx, dy) <= range_size
