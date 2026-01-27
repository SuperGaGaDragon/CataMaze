"""
Extract local 5x5 vision from global map.
"""
from typing import List, Tuple, Dict


def extract_local_vision(
    grid: List[List[str]],
    center_pos: Tuple[int, int],
    vision_size: int = 5
) -> List[List[str]]:
    """
    Extract 5x5 (or custom size) vision centered on a position.
    Out-of-bounds cells are filled with '#' (wall).

    Args:
        grid: Full 50x50 map
        center_pos: (x, y) center position
        vision_size: Size of vision grid (default 5, must be odd)

    Returns:
        vision_size x vision_size 2D array

    Raises:
        ValueError: If vision_size is not odd
    """
    if vision_size % 2 == 0:
        raise ValueError(f"vision_size must be odd, got {vision_size}")

    cx, cy = center_pos
    radius = vision_size // 2

    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    vision = []
    for dy in range(-radius, radius + 1):
        row = []
        for dx in range(-radius, radius + 1):
            x = cx + dx
            y = cy + dy

            # Check bounds
            if 0 <= x < width and 0 <= y < height:
                row.append(grid[y][x])
            else:
                # Out of bounds = wall
                row.append('#')

        vision.append(row)

    return vision


def render_vision_with_entities(
    vision: List[List[str]],
    center_pos: Tuple[int, int],
    other_entities: Dict[str, Tuple[int, int]],
    vision_size: int = 5
) -> List[List[str]]:
    """
    Render vision with entities marked.
    Center position is marked as '@' (self).
    Other entities in vision are marked as 'P' (player/agent).

    Args:
        vision: Base vision grid from extract_local_vision
        center_pos: (x, y) center entity position
        other_entities: Dict of {entity_id: (x, y)} for other entities
        vision_size: Size of vision grid (default 5)

    Returns:
        vision_size x vision_size 2D array with entity markers
    """
    # Deep copy vision to avoid modifying original
    rendered = [row[:] for row in vision]

    cx, cy = center_pos
    radius = vision_size // 2

    # Mark center as '@' (self)
    center_idx = radius  # Middle of 5x5 is index 2
    rendered[center_idx][center_idx] = '@'

    # Mark other entities as 'P' if in vision range
    for entity_id, (ex, ey) in other_entities.items():
        # Calculate relative position
        dx = ex - cx
        dy = ey - cy

        # Check if in vision range
        if abs(dx) <= radius and abs(dy) <= radius:
            # Convert to vision grid coordinates
            vision_x = radius + dx
            vision_y = radius + dy

            # Mark as 'P' (unless it's a wall, which shouldn't happen)
            if rendered[vision_y][vision_x] != '#':
                rendered[vision_y][vision_x] = 'P'

    return rendered


def get_vision_for_entity(
    grid: List[List[str]],
    entity_pos: Tuple[int, int],
    all_entities: Dict[str, Tuple[int, int]],
    entity_id: str,
    vision_size: int = 5
) -> List[List[str]]:
    """
    Get complete vision for an entity, including other entities.

    Args:
        grid: Full map
        entity_pos: (x, y) position of the entity
        all_entities: Dict of {entity_id: (x, y)} for all entities
        entity_id: ID of the entity viewing
        vision_size: Size of vision (default 5)

    Returns:
        Rendered vision with '@' for self, 'P' for others
    """
    # Extract base vision
    vision = extract_local_vision(grid, entity_pos, vision_size)

    # Get other entities (exclude self)
    other_entities = {
        eid: pos for eid, pos in all_entities.items()
        if eid != entity_id
    }

    # Render with entities
    return render_vision_with_entities(vision, entity_pos, other_entities, vision_size)
