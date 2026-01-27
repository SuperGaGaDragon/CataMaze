"""
Action definitions and direction vectors.
"""
from typing import Tuple, Dict

# Action type definitions
MOVE_UP = "MOVE_UP"
MOVE_DOWN = "MOVE_DOWN"
MOVE_LEFT = "MOVE_LEFT"
MOVE_RIGHT = "MOVE_RIGHT"

SHOOT_UP = "SHOOT_UP"
SHOOT_DOWN = "SHOOT_DOWN"
SHOOT_LEFT = "SHOOT_LEFT"
SHOOT_RIGHT = "SHOOT_RIGHT"

WAIT = "WAIT"

# All valid actions
ALL_ACTIONS = [
    MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT,
    SHOOT_UP, SHOOT_DOWN, SHOOT_LEFT, SHOOT_RIGHT,
    WAIT
]

# Movement actions only
MOVE_ACTIONS = [MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT]

# Shoot actions only
SHOOT_ACTIONS = [SHOOT_UP, SHOOT_DOWN, SHOOT_LEFT, SHOOT_RIGHT]

# Direction vectors: action -> (dx, dy)
# Note: y increases downward (row index), x increases rightward (column index)
DIRECTION_VECTORS: Dict[str, Tuple[int, int]] = {
    MOVE_UP: (0, -1),
    MOVE_DOWN: (0, 1),
    MOVE_LEFT: (-1, 0),
    MOVE_RIGHT: (1, 0),
    SHOOT_UP: (0, -1),
    SHOOT_DOWN: (0, 1),
    SHOOT_LEFT: (-1, 0),
    SHOOT_RIGHT: (1, 0),
}

# Extract direction from action
DIRECTION_FROM_ACTION: Dict[str, str] = {
    MOVE_UP: "UP",
    MOVE_DOWN: "DOWN",
    MOVE_LEFT: "LEFT",
    MOVE_RIGHT: "RIGHT",
    SHOOT_UP: "UP",
    SHOOT_DOWN: "DOWN",
    SHOOT_LEFT: "LEFT",
    SHOOT_RIGHT: "RIGHT",
}


def is_move_action(action: str) -> bool:
    """Check if action is a movement action."""
    return action in MOVE_ACTIONS


def is_shoot_action(action: str) -> bool:
    """Check if action is a shoot action."""
    return action in SHOOT_ACTIONS


def is_wait_action(action: str) -> bool:
    """Check if action is wait."""
    return action == WAIT


def is_valid_action(action: str) -> bool:
    """Check if action is valid."""
    return action in ALL_ACTIONS


def get_direction_vector(action: str) -> Tuple[int, int]:
    """
    Get direction vector for an action.

    Args:
        action: Action string

    Returns:
        (dx, dy) tuple

    Raises:
        ValueError: If action has no direction (e.g., WAIT)
    """
    if action not in DIRECTION_VECTORS:
        raise ValueError(f"Action {action} has no direction vector")
    return DIRECTION_VECTORS[action]


def get_direction_name(action: str) -> str:
    """
    Get direction name from action.

    Args:
        action: Action string

    Returns:
        Direction name: "UP", "DOWN", "LEFT", "RIGHT"

    Raises:
        ValueError: If action has no direction
    """
    if action not in DIRECTION_FROM_ACTION:
        raise ValueError(f"Action {action} has no direction")
    return DIRECTION_FROM_ACTION[action]
