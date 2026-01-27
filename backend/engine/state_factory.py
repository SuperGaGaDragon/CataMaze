"""
Factory functions for creating initial game states.
"""
import random
import uuid
from typing import List, Tuple, Optional

from backend.engine.state import WorldState, create_entity
from backend.maps.loader import load_map, get_start_and_exit
from backend.engine.position import is_walkable


def find_random_walkable_position(
    grid: List[List[str]],
    exclude_positions: List[Tuple[int, int]]
) -> Tuple[int, int]:
    """
    Find a random walkable position that's not in exclude list.

    Args:
        grid: Map grid
        exclude_positions: Positions to avoid

    Returns:
        (x, y) random walkable position

    Raises:
        RuntimeError: If no walkable position found after many attempts
    """
    width = len(grid[0])
    height = len(grid)

    for _ in range(1000):  # Try max 1000 times
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        pos = (x, y)

        if pos not in exclude_positions and is_walkable(grid, pos):
            return pos

    raise RuntimeError("Could not find random walkable position after 1000 attempts")


def create_new_state(map_name: str = "map1.txt", game_id: Optional[str] = None) -> WorldState:
    """
    Create a new game state with random entity placement.

    Args:
        map_name: Name of map file to load
        game_id: Optional game ID (generates UUID if not provided)

    Returns:
        WorldState with player and 3 agents randomly placed
    """
    # Load map
    grid = load_map(map_name)
    (start_x, start_y), (exit_x, exit_y) = get_start_and_exit(grid)

    # Generate game ID
    if game_id is None:
        game_id = str(uuid.uuid4())

    # Track used positions
    used_positions = [(start_x, start_y), (exit_x, exit_y)]

    # Create player at random position
    player_pos = find_random_walkable_position(grid, used_positions)
    used_positions.append(player_pos)

    player = create_entity(
        entity_id="player",
        entity_type="player",
        x=player_pos[0],
        y=player_pos[1],
        persona=None
    )

    # Create 3 agents with different personas
    personas = ["aggressive", "cautious", "explorer"]
    agents = {}

    for i, persona in enumerate(personas):
        agent_pos = find_random_walkable_position(grid, used_positions)
        used_positions.append(agent_pos)

        agent_id = f"agent_{persona}_{i+1}"
        agent = create_entity(
            entity_id=agent_id,
            entity_type="agent",
            x=agent_pos[0],
            y=agent_pos[1],
            persona=persona
        )
        agents[agent_id] = agent

    # Combine all entities
    entities = {"player": player, **agents}

    # Create world state
    return WorldState(
        game_id=game_id,
        tick=0,
        map_grid=grid,
        start_x=start_x,
        start_y=start_y,
        exit_x=exit_x,
        exit_y=exit_y,
        entities=entities,
        bullets=[],
        game_over=False,
        winner_id=None
    )
