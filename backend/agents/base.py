"""
Base Agent Interface for CataMaze
"""
from abc import ABC, abstractmethod
from typing import Optional


class Agent(ABC):
    """Base class for all agents"""

    def __init__(self, entity_id: str, persona: Optional[str] = None):
        self.entity_id = entity_id
        self.persona = persona

    @abstractmethod
    def decide_action(self, observation: dict) -> str:
        """
        Decide next action based on observation.

        Args:
            observation: Current game observation for this agent

        Returns:
            action: One of MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT,
                   SHOOT_UP, SHOOT_DOWN, SHOOT_LEFT, SHOOT_RIGHT, WAIT
        """
        pass

    def reset(self):
        """Reset agent state (optional)"""
        pass
