"""
Bullet and ammo management module.
Handles ammo count, recovery, shooting, and bullet hit detection.
"""
from typing import Tuple, List, Optional
from .constants import (
    INITIAL_AMMO, MAX_AMMO, MIN_AMMO,
    AMMO_RECOVERY_TICKS
)
from .position import add_vector, is_in_bounds


def create_ammo_state(initial_ammo: int = INITIAL_AMMO) -> int:
    """
    Create initial ammo state.

    Args:
        initial_ammo: Starting ammo count

    Returns:
        Ammo value
    """
    return min(max(initial_ammo, MIN_AMMO), MAX_AMMO)


def can_shoot(ammo: int) -> bool:
    """
    Check if entity can shoot.

    Args:
        ammo: Current ammo count

    Returns:
        True if ammo > 0, False otherwise
    """
    return ammo > MIN_AMMO


def consume_ammo(current_ammo: int) -> int:
    """
    Consume 1 ammo for shooting.

    Args:
        current_ammo: Current ammo count

    Returns:
        New ammo count (clamped to MIN_AMMO)
    """
    if can_shoot(current_ammo):
        return current_ammo - 1
    return current_ammo


def should_recover_ammo(current_tick: int, last_shot_tick: int) -> bool:
    """
    Check if ammo should be recovered.
    Ammo recovers every AMMO_RECOVERY_TICKS (2 ticks).

    Args:
        current_tick: Current game tick
        last_shot_tick: Tick when last bullet was fired

    Returns:
        True if enough ticks have passed, False otherwise
    """
    ticks_since_shot = current_tick - last_shot_tick
    return ticks_since_shot >= AMMO_RECOVERY_TICKS


def recover_ammo(current_ammo: int, current_tick: int, last_shot_tick: int) -> Tuple[int, int]:
    """
    Recover ammo if conditions are met.

    Args:
        current_ammo: Current ammo count
        current_tick: Current game tick
        last_shot_tick: Tick when last bullet was fired

    Returns:
        (new_ammo, new_last_shot_tick) tuple
        - new_ammo: Recovered ammo count
        - new_last_shot_tick: Updated last shot tick (advances by AMMO_RECOVERY_TICKS)
    """
    if current_ammo >= MAX_AMMO:
        return current_ammo, last_shot_tick

    if should_recover_ammo(current_tick, last_shot_tick):
        new_ammo = min(current_ammo + 1, MAX_AMMO)
        new_last_shot_tick = last_shot_tick + AMMO_RECOVERY_TICKS
        return new_ammo, new_last_shot_tick

    return current_ammo, last_shot_tick


# Bullet trajectory calculation


def trace_bullet_path(
    start_pos: Tuple[int, int],
    direction_vector: Tuple[int, int],
    grid: List[List[str]],
    max_range: int = 50
) -> List[Tuple[int, int]]:
    """
    Trace the path of a bullet until it hits a wall or edge.

    Args:
        start_pos: (x, y) starting position
        direction_vector: (dx, dy) direction
        grid: Map grid
        max_range: Maximum bullet travel distance

    Returns:
        List of (x, y) positions the bullet travels through
    """
    path = []
    current_pos = start_pos

    for _ in range(max_range):
        next_pos = add_vector(current_pos, direction_vector)

        # Check if out of bounds
        if not is_in_bounds(next_pos, len(grid[0]), len(grid)):
            break

        x, y = next_pos
        cell = grid[y][x]

        # Hit a wall
        if cell == '#':
            break

        # Add position to path
        path.append(next_pos)
        current_pos = next_pos

    return path


def check_bullet_hit(
    bullet_path: List[Tuple[int, int]],
    entity_positions: List[Tuple[int, int]]
) -> Optional[Tuple[int, int]]:
    """
    Check if a bullet hits any entity.

    Args:
        bullet_path: List of positions bullet travels through
        entity_positions: List of entity positions to check

    Returns:
        Position of first entity hit, or None if no hit
    """
    for bullet_pos in bullet_path:
        if bullet_pos in entity_positions:
            return bullet_pos
    return None


def simulate_shot(
    shooter_pos: Tuple[int, int],
    direction_vector: Tuple[int, int],
    grid: List[List[str]],
    target_positions: List[Tuple[int, int]]
) -> Optional[Tuple[int, int]]:
    """
    Simulate a shot and return hit position if any.

    Args:
        shooter_pos: (x, y) shooter position
        direction_vector: (dx, dy) shoot direction
        grid: Map grid
        target_positions: List of possible target positions

    Returns:
        Position of hit target, or None if no hit
    """
    # Bullet starts one cell away from shooter
    bullet_start = add_vector(shooter_pos, direction_vector)

    # Trace bullet path
    path = trace_bullet_path(bullet_start, direction_vector, grid)

    # Check for hits
    return check_bullet_hit(path, target_positions)
