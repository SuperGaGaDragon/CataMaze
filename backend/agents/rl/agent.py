"""
RL Agent Implementation
"""
from backend.agents.base import Agent
from backend.agents.rl.encoder import ObservationEncoder
from backend.agents.rl.policy import Policy
from backend.agents.rl.reward import RewardCalculator
from backend.agents.rl.action_mask import ActionMask
import json
import os


class RLAgent(Agent):
    """Reinforcement Learning Agent"""

    def __init__(self, entity_id: str, persona: str = "aggressive"):
        super().__init__(entity_id, persona)

        # Load persona configuration
        persona_path = f"backend/personas/{persona}.json"
        if os.path.exists(persona_path):
            with open(persona_path, 'r') as f:
                self.persona_config = json.load(f)
        else:
            self.persona_config = self._default_config()

        # Initialize components
        self.encoder = ObservationEncoder()
        self.policy = Policy(persona=persona)
        self.reward_calc = RewardCalculator()
        self.action_mask = ActionMask()

        # Agent state
        self.last_observation = None
        self.last_action = None
        self.episode_reward = 0.0

    def _default_config(self):
        """Default persona configuration"""
        return {
            "behavior": {
                "shoot_probability": 0.5,
                "chase_probability": 0.5,
                "explore_probability": 0.5,
                "flee_probability": 0.3
            }
        }

    def decide_action(self, observation: dict) -> str:
        """
        Decide action using RL policy.

        Args:
            observation: Current game observation

        Returns:
            action: Selected action string
        """
        # Encode observation to feature vector
        features = self.encoder.encode(observation)

        # Get valid actions mask
        valid_actions = self.action_mask.get_valid_actions(observation)

        # Select action from policy
        action = self.policy.select_action(features, valid_actions, self.persona_config)

        # Store for learning
        self.last_observation = observation
        self.last_action = action

        return action

    def update(self, reward: float, next_observation: dict, done: bool):
        """
        Update policy based on reward (for training).

        Args:
            reward: Reward received
            next_observation: Next observation
            done: Whether episode is done
        """
        if self.last_observation is None:
            return

        # Calculate total reward
        calculated_reward = self.reward_calc.calculate(
            self.last_observation,
            self.last_action,
            next_observation,
            done
        )

        total_reward = reward + calculated_reward
        self.episode_reward += total_reward

        # Update policy (placeholder for actual RL update)
        # In full implementation: update neural network, replay buffer, etc.

        if done:
            self.episode_reward = 0.0
            self.last_observation = None
            self.last_action = None

    def reset(self):
        """Reset agent state"""
        self.last_observation = None
        self.last_action = None
        self.episode_reward = 0.0
        self.policy.reset()
