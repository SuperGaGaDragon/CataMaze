"""
Policy for RL Agent

Implements action selection strategy based on features and persona.
"""
import numpy as np
from typing import Dict, List
import random


class Policy:
    """Action selection policy for RL agent"""

    def __init__(self, persona: str = "aggressive"):
        """
        Initialize policy.

        Args:
            persona: Agent persona name
        """
        self.persona = persona

        # Action space
        self.actions = [
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

        # Exploration parameters
        self.epsilon = 0.1  # Exploration rate
        self.temperature = 1.0  # Softmax temperature

    def select_action(
        self,
        features: np.ndarray,
        valid_actions: List[str],
        persona_config: Dict
    ) -> str:
        """
        Select action based on features and persona.

        Args:
            features: Encoded observation features
            valid_actions: List of valid action strings
            persona_config: Persona configuration dict

        Returns:
            action: Selected action string
        """
        # Filter valid actions
        valid_action_indices = [
            i for i, action in enumerate(self.actions)
            if action in valid_actions
        ]

        if not valid_action_indices:
            return "wait"

        # Epsilon-greedy exploration
        if random.random() < self.epsilon:
            # Random exploration
            idx = random.choice(valid_action_indices)
            return self.actions[idx]

        # Policy-based selection
        action_scores = self._compute_action_scores(
            features,
            valid_action_indices,
            persona_config
        )

        # Apply softmax with temperature
        probs = self._softmax(action_scores, self.temperature)

        # Sample from distribution
        idx = np.random.choice(valid_action_indices, p=probs)
        return self.actions[idx]

    def _compute_action_scores(
        self,
        features: np.ndarray,
        valid_indices: List[int],
        persona_config: Dict
    ) -> np.ndarray:
        """
        Compute action scores based on heuristics and persona.

        Args:
            features: Observation features
            valid_indices: Valid action indices
            persona_config: Persona configuration

        Returns:
            scores: Score for each valid action
        """
        scores = np.zeros(len(valid_indices))

        # Extract persona weights
        behavior = persona_config.get("behavior", {})
        decision_weights = persona_config.get("decision_weights", {})
        thresholds = persona_config.get("thresholds", {})

        # Parse features (basic heuristic)
        # Self state starts at index 100 (5*5*4)
        hp = features[100] if len(features) > 100 else 0.5
        ammo = features[101] if len(features) > 101 else 0.5

        # Heuristic scoring for each action
        for i, action_idx in enumerate(valid_indices):
            action = self.actions[action_idx]
            score = 0.0

            # Movement actions
            if action.startswith("MOVE_"):
                score += decision_weights.get("explore", 0.5)

                # Prefer exploration when hp is high
                if hp > 0.6:
                    score += 0.3
                else:
                    # Prefer fleeing when hp is low
                    score += decision_weights.get("flee", 0.3)

            # Shooting actions
            elif action.startswith("SHOOT_"):
                score += decision_weights.get("attack", 0.5)

                # Can only shoot if we have ammo
                if ammo > 0:
                    score += behavior.get("shoot_probability", 0.5)
                else:
                    score = 0.0  # Invalid if no ammo

                # Reduce shooting when low hp (cautious behavior)
                min_hp = thresholds.get("min_hp_to_attack", 2) / 5.0
                if hp < min_hp:
                    score *= 0.5

            # Wait action
            elif action == "WAIT":
                score += 0.1

                # Prefer waiting when low ammo (to recover)
                if ammo < 0.3:
                    score += 0.4

            scores[i] = score

        # Normalize to prevent negative scores
        scores = np.maximum(scores, 0.01)

        return scores

    def _softmax(self, scores: np.ndarray, temperature: float = 1.0) -> np.ndarray:
        """
        Apply softmax to scores.

        Args:
            scores: Action scores
            temperature: Temperature parameter (higher = more random)

        Returns:
            probs: Probability distribution
        """
        # Scale by temperature
        scaled_scores = scores / temperature

        # Compute softmax
        exp_scores = np.exp(scaled_scores - np.max(scaled_scores))
        probs = exp_scores / np.sum(exp_scores)

        return probs

    def reset(self):
        """Reset policy state (for episodic agents)"""
        # In future: reset neural network hidden states
        pass

    def update_epsilon(self, new_epsilon: float):
        """
        Update exploration rate.

        Args:
            new_epsilon: New epsilon value
        """
        self.epsilon = max(0.0, min(1.0, new_epsilon))

    def update_temperature(self, new_temp: float):
        """
        Update softmax temperature.

        Args:
            new_temp: New temperature value
        """
        self.temperature = max(0.1, new_temp)
