"""
Observation generation for entities.
Creates the observation dict that entities see.
"""
from typing import Dict, Any, Optional, Tuple
from engine.state import WorldState, EntityState
from engine.local_map import get_vision_for_entity
from engine.position import is_in_range
from engine.constants import SOUND_RANGE


def generate_observation(
    world: WorldState,
    entity_id: str,
    last_sound: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate observation for an entity.

    Args:
        world: Current world state
        entity_id: ID of the entity to generate observation for
        last_sound: Optional last sound heard

    Returns:
        Observation dict with vision, stats, and status
    """
    entity = world.entities[entity_id]

    # Get all entity positions for vision rendering
    all_positions = {
        eid: (e.x, e.y)
        for eid, e in world.entities.items()
        if e.alive  # Only show alive entities
    }

    # Generate vision
    vision = get_vision_for_entity(
        world.map_grid,
        (entity.x, entity.y),
        all_positions,
        entity_id
    )

    # Build observation
    obs = {
        "entity_id": entity_id,
        "hp": entity.hp,
        "ammo": entity.ammo,
        "time": world.tick,
        "position": {
            "x": entity.x,
            "y": entity.y
        },
        "vision": vision,
        "last_sound": last_sound,
        "alive": entity.alive,
        "won": entity.won,
        "game_over": world.game_over
    }

    return obs


def check_sound_in_range(
    listener_pos: Tuple[int, int],
    shooter_pos: Tuple[int, int]
) -> bool:
    """
    Check if a shot can be heard by a listener.

    Args:
        listener_pos: (x, y) position of listener
        shooter_pos: (x, y) position of shooter

    Returns:
        True if within sound range (7x7 = range 3)
    """
    return is_in_range(listener_pos, shooter_pos, SOUND_RANGE)


def generate_sound_for_entity(
    entity_pos: Tuple[int, int],
    shot_positions: list[Tuple[int, int]]
) -> Optional[str]:
    """
    Generate sound observation for an entity based on nearby shots.

    Args:
        entity_pos: (x, y) position of the entity
        shot_positions: List of positions where shots were fired

    Returns:
        "*click*" if shots heard, None otherwise
    """
    for shot_pos in shot_positions:
        if check_sound_in_range(entity_pos, shot_pos):
            return "*click*"
    return None
