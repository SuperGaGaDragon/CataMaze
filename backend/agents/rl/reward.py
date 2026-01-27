"""
Reward Calculator for RL Agent

Calculates dense rewards to guide agent learning.
"""
from typing import Dict


class RewardCalculator:
    """Calculates rewards for RL training"""

    def __init__(self):
        """Initialize reward calculator with reward weights"""
        # Reward weights
        self.weights = {
            # Survival
            "alive": 0.01,          # Small reward for staying alive
            "hp_gain": 1.0,         # Reward for gaining HP
            "hp_loss": -2.0,        # Penalty for losing HP
            "death": -10.0,         # Large penalty for dying

            # Combat
            "hit_enemy": 3.0,       # Reward for hitting enemy
            "kill_enemy": 5.0,      # Large reward for killing enemy
            "got_hit": -2.0,        # Penalty for getting hit
            "shoot_miss": -0.1,     # Small penalty for wasting ammo

            # Resources
            "ammo_gain": 0.5,       # Reward for gaining ammo
            "ammo_recover": 0.3,    # Reward for ammo auto-recovery
            "pickup_item": 1.0,     # Reward for picking up items

            # Exploration
            "explore_new": 0.5,     # Reward for exploring new cells
            "revisit": -0.05,       # Small penalty for revisiting

            # Win/Loss
            "win": 100.0,           # Huge reward for winning
            "loss": -50.0,          # Large penalty for losing
        }

    def calculate(
        self,
        prev_obs: Dict,
        action: str,
        next_obs: Dict,
        done: bool
    ) -> float:
        """
        Calculate reward for transition.

        Args:
            prev_obs: Previous observation
            action: Action taken
            next_obs: Next observation
            done: Whether episode ended

        Returns:
            reward: Calculated reward value
        """
        total_reward = 0.0

        # Extract states
        prev_hp = prev_obs.get("hp", 0)
        next_hp = next_obs.get("hp", 0)
        prev_ammo = prev_obs.get("ammo", 0)
        next_ammo = next_obs.get("ammo", 0)

        # Survival rewards
        if not done:
            total_reward += self.weights["alive"]

        # HP changes
        hp_diff = next_hp - prev_hp
        if hp_diff > 0:
            total_reward += self.weights["hp_gain"] * hp_diff
        elif hp_diff < 0:
            total_reward += self.weights["hp_loss"] * abs(hp_diff)

        # Death penalty
        if done and next_hp <= 0:
            total_reward += self.weights["death"]

        # Ammo changes
        ammo_diff = next_ammo - prev_ammo
        if ammo_diff > 0:
            # Check if it's auto-recovery or pickup
            if "ammo_recovered" in next_obs.get("events", []):
                total_reward += self.weights["ammo_recover"]
            else:
                total_reward += self.weights["ammo_gain"] * ammo_diff
        elif ammo_diff < 0:
            # Used ammo - check if we hit anything
            events = next_obs.get("events", [])
            if "hit_enemy" in events:
                total_reward += self.weights["hit_enemy"]
            elif "killed_enemy" in events:
                total_reward += self.weights["kill_enemy"]
            else:
                # Missed shot
                total_reward += self.weights["shoot_miss"]

        # Getting hit
        if "got_hit" in next_obs.get("events", []):
            total_reward += self.weights["got_hit"]

        # Item pickups
        if "picked_up_health" in next_obs.get("events", []):
            total_reward += self.weights["pickup_item"]
        if "picked_up_ammo" in next_obs.get("events", []):
            total_reward += self.weights["pickup_item"]

        # Exploration rewards
        prev_pos = prev_obs.get("position", {})
        next_pos = next_obs.get("position", {})
        if prev_pos != next_pos:
            # Check if explored new area (simplified)
            if "explored_new" in next_obs.get("events", []):
                total_reward += self.weights["explore_new"]
            else:
                total_reward += self.weights["revisit"]

        # Win/Loss terminal rewards
        if done:
            status = next_obs.get("status", "")
            if status == "won":
                total_reward += self.weights["win"]
            elif status == "lost":
                total_reward += self.weights["loss"]

        return total_reward

    def update_weights(self, new_weights: Dict[str, float]):
        """
        Update reward weights.

        Args:
            new_weights: Dictionary of reward weights to update
        """
        for key, value in new_weights.items():
            if key in self.weights:
                self.weights[key] = value

    def get_weights(self) -> Dict[str, float]:
        """Get current reward weights"""
        return self.weights.copy()
