"""
Map loader module.
Reads 50x50 maze from text file.
"""
import os
from typing import List, Tuple, Optional


def load_map(map_name: str = "map1.txt") -> List[List[str]]:
    """
    Load map from file and return as 2D array.

    Args:
        map_name: Name of map file (default: map1.txt)

    Returns:
        50x50 2D list of characters

    Raises:
        FileNotFoundError: If map file doesn't exist
        ValueError: If map is not 50x50
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    map_path = os.path.join(current_dir, map_name)

    if not os.path.exists(map_path):
        raise FileNotFoundError(f"Map file not found: {map_path}")

    with open(map_path, 'r') as f:
        lines = f.readlines()

    # Remove trailing newlines and convert to 2D array
    grid = []
    for line in lines:
        line = line.rstrip('\n')
        if line:  # Skip empty lines
            grid.append(list(line))

    # Validate map size
    if len(grid) != 50:
        raise ValueError(f"Map must have 50 rows, got {len(grid)}")

    for i, row in enumerate(grid):
        if len(row) != 50:
            raise ValueError(f"Row {i} must have 50 columns, got {len(row)}")

    return grid


def find_position(grid: List[List[str]], target: str) -> Optional[Tuple[int, int]]:
    """
    Find position of a specific character in the grid.

    Args:
        grid: 2D array
        target: Character to find ('S' for start, 'E' for exit)

    Returns:
        (x, y) tuple if found, None otherwise
    """
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == target:
                return (x, y)
    return None


def get_start_and_exit(grid: List[List[str]]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Find start (S) and exit (E) positions.

    Args:
        grid: 2D array

    Returns:
        ((start_x, start_y), (exit_x, exit_y))

    Raises:
        ValueError: If start or exit not found
    """
    start_pos = find_position(grid, 'S')
    exit_pos = find_position(grid, 'E')

    if start_pos is None:
        raise ValueError("Start position 'S' not found in map")
    if exit_pos is None:
        raise ValueError("Exit position 'E' not found in map")

    return start_pos, exit_pos
