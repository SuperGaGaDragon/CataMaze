"""
HP management module.
Handles health points, damage, and death determination.
"""
from .constants import INITIAL_HP, MAX_HP, MIN_HP, BULLET_DAMAGE


def create_hp_state(initial_hp: int = INITIAL_HP) -> int:
    """
    Create initial HP state.

    Args:
        initial_hp: Starting HP (default from constants)

    Returns:
        HP value
    """
    return min(max(initial_hp, MIN_HP), MAX_HP)


def take_damage(current_hp: int, damage: int = BULLET_DAMAGE) -> int:
    """
    Apply damage to HP.

    Args:
        current_hp: Current HP value
        damage: Damage amount (default 1 bullet damage)

    Returns:
        New HP value (clamped to MIN_HP)
    """
    new_hp = current_hp - damage
    return max(new_hp, MIN_HP)


def is_alive(hp: int) -> bool:
    """
    Check if entity is alive.

    Args:
        hp: Current HP value

    Returns:
        True if HP > 0, False otherwise
    """
    return hp > MIN_HP


def is_dead(hp: int) -> bool:
    """
    Check if entity is dead.

    Args:
        hp: Current HP value

    Returns:
        True if HP <= 0, False otherwise
    """
    return hp <= MIN_HP


def get_hp_percentage(current_hp: int) -> float:
    """
    Get HP as percentage.

    Args:
        current_hp: Current HP value

    Returns:
        HP percentage (0.0 to 1.0)
    """
    return current_hp / MAX_HP if MAX_HP > 0 else 0.0


def apply_hit(current_hp: int, hit_count: int = 1) -> tuple[int, bool]:
    """
    Apply multiple hits and check if entity died.

    Args:
        current_hp: Current HP value
        hit_count: Number of hits (default 1)

    Returns:
        (new_hp, died) tuple
        - new_hp: HP after damage
        - died: True if entity died from this hit
    """
    was_alive = is_alive(current_hp)
    new_hp = take_damage(current_hp, BULLET_DAMAGE * hit_count)
    died = was_alive and is_dead(new_hp)
    return new_hp, died
