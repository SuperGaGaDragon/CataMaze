"""
Action Mask for RL Agent

Determines which actions are valid in the current game state.
"""
from typing import Dict, List


class ActionMask:
    """Generates valid action masks for RL agent"""

    def __init__(self):
        """Initialize action mask generator"""
        # All possible actions
        self.all_actions = [
            "MOVE_UP",
            "MOVE_DOWN",
            "MOVE_LEFT",
            "MOVE_RIGHT",
            "SHOOT_UP",
            "SHOOT_DOWN",
            "SHOOT_LEFT",
            "SHOOT_RIGHT",
            "WAIT"
        ]

    def get_valid_actions(self, observation: Dict) -> List[str]:
        """
        Get list of valid actions for current state.

        Args:
            observation: Current game observation

        Returns:
            valid_actions: List of valid action strings
        """
        valid_actions = []

        # Extract state information
        position = observation.get("position", {"x": 0, "y": 0})
        vision = observation.get("vision", [])
        ammo = observation.get("ammo", 0)
        hp = observation.get("hp", 0)

        # Dead agents can't act
        if hp <= 0:
            return ["WAIT"]

        # Check movement actions
        if self._can_move_north(position, vision):
            valid_actions.append("MOVE_UP")

        if self._can_move_south(position, vision):
            valid_actions.append("MOVE_DOWN")

        if self._can_move_east(position, vision):
            valid_actions.append("MOVE_RIGHT")

        if self._can_move_west(position, vision):
            valid_actions.append("MOVE_LEFT")

        # Check shooting actions (need ammo)
        if ammo > 0:
            valid_actions.extend([
                "SHOOT_UP",
                "SHOOT_DOWN",
                "SHOOT_LEFT",
                "SHOOT_RIGHT"
            ])

        # Wait is always valid
        valid_actions.append("WAIT")

        return valid_actions

    def _can_move_north(self, position: Dict, vision: List[List[str]]) -> bool:
        """
        Check if can move north.

        Args:
            position: Current position
            vision: 5x5 vision grid

        Returns:
            can_move: True if movement is valid
        """
        # Check map boundaries
        y = position.get("y", 0)
        if y <= 0:
            return False

        # Check vision grid (center is [2][2])
        if vision and len(vision) >= 3 and len(vision[0]) >= 3:
            # North is [1][2]
            north_cell = vision[1][2]
            if north_cell == '#':  # Wall
                return False

        return True

    def _can_move_south(self, position: Dict, vision: List[List[str]]) -> bool:
        """
        Check if can move south.

        Args:
            position: Current position
            vision: 5x5 vision grid

        Returns:
            can_move: True if movement is valid
        """
        # Check map boundaries
        y = position.get("y", 0)
        if y >= 49:  # Map is 50x50 (0-49)
            return False

        # Check vision grid
        if vision and len(vision) >= 4 and len(vision[0]) >= 3:
            # South is [3][2]
            south_cell = vision[3][2]
            if south_cell == '#':  # Wall
                return False

        return True

    def _can_move_east(self, position: Dict, vision: List[List[str]]) -> bool:
        """
        Check if can move east.

        Args:
            position: Current position
            vision: 5x5 vision grid

        Returns:
            can_move: True if movement is valid
        """
        # Check map boundaries
        x = position.get("x", 0)
        if x >= 49:  # Map is 50x50 (0-49)
            return False

        # Check vision grid
        if vision and len(vision) >= 3 and len(vision[2]) >= 4:
            # East is [2][3]
            east_cell = vision[2][3]
            if east_cell == '#':  # Wall
                return False

        return True

    def _can_move_west(self, position: Dict, vision: List[List[str]]) -> bool:
        """
        Check if can move west.

        Args:
            position: Current position
            vision: 5x5 vision grid

        Returns:
            can_move: True if movement is valid
        """
        # Check map boundaries
        x = position.get("x", 0)
        if x <= 0:
            return False

        # Check vision grid
        if vision and len(vision) >= 3 and len(vision[2]) >= 2:
            # West is [2][1]
            west_cell = vision[2][1]
            if west_cell == '#':  # Wall
                return False

        return True

    def get_action_mask_binary(self, observation: Dict) -> List[int]:
        """
        Get binary action mask (for neural networks).

        Args:
            observation: Current game observation

        Returns:
            mask: Binary list [1 if valid, 0 if invalid] for all actions
        """
        valid_actions = self.get_valid_actions(observation)

        mask = [
            1 if action in valid_actions else 0
            for action in self.all_actions
        ]

        return mask
