"""
Human Agent - uses action queue
"""
from backend.agents.base import Agent


class HumanAgent(Agent):
    """Human-controlled agent that uses action queue"""

    def __init__(self, entity_id: str):
        super().__init__(entity_id, persona="human")

    def decide_action(self, observation: dict) -> str:
        """
        Human agents don't use this method.
        Actions come from the player's action_queue.
        """
        return "WAIT"
