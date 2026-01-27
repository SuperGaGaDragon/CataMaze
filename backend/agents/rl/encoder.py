"""
Observation Encoder for RL Agent

Converts game observations into numerical feature vectors
for neural network processing.
"""
import numpy as np
from typing import Dict, List


class ObservationEncoder:
    """Encodes game observations into feature vectors"""

    def __init__(self):
        """Initialize encoder with feature dimensions"""
        # Feature dimensions
        self.vision_size = 5  # 5x5 grid
        self.max_entities = 10  # Max entities to track
        self.feature_dim = self._calculate_feature_dim()

    def _calculate_feature_dim(self) -> int:
        """Calculate total feature dimension"""
        # Vision grid: 5x5 cells * 4 channels (wall, entity, item, bullet)
        vision_features = self.vision_size * self.vision_size * 4

        # Self state: hp, ammo, position (x, y)
        self_features = 4

        # Nearby entities: position, distance, angle (3 features * max_entities)
        entity_features = 3 * self.max_entities

        # Sounds: direction encoding (8 directions)
        sound_features = 8

        return vision_features + self_features + entity_features + sound_features

    def encode(self, observation: Dict) -> np.ndarray:
        """
        Encode observation into feature vector.

        Args:
            observation: Game observation dict

        Returns:
            features: Numpy array of encoded features
        """
        features = []

        # Encode vision grid
        vision_features = self._encode_vision(observation.get("vision", []))
        features.extend(vision_features)

        # Encode self state
        self_features = self._encode_self_state(observation)
        features.extend(self_features)

        # Encode nearby entities
        entity_features = self._encode_entities(observation.get("entities", []))
        features.extend(entity_features)

        # Encode sounds
        sound_features = self._encode_sounds(observation.get("sounds", []))
        features.extend(sound_features)

        return np.array(features, dtype=np.float32)

    def _encode_vision(self, vision_grid: List[List[str]]) -> List[float]:
        """
        Encode 5x5 vision grid into features.

        Args:
            vision_grid: 5x5 grid of cell contents

        Returns:
            features: Flattened vision features
        """
        features = []

        # If vision is empty, return zeros
        if not vision_grid or len(vision_grid) != self.vision_size:
            return [0.0] * (self.vision_size * self.vision_size * 4)

        for row in vision_grid:
            for cell in row:
                # 4 binary channels per cell
                is_wall = 1.0 if cell == '#' else 0.0
                is_entity = 1.0 if cell in ['@', 'E'] else 0.0
                is_item = 1.0 if cell in ['H', 'A'] else 0.0
                is_bullet = 1.0 if cell == '*' else 0.0

                features.extend([is_wall, is_entity, is_item, is_bullet])

        return features

    def _encode_self_state(self, observation: Dict) -> List[float]:
        """
        Encode agent's own state.

        Args:
            observation: Game observation

        Returns:
            features: [hp_normalized, ammo_normalized, x_normalized, y_normalized]
        """
        # Normalize values to [0, 1]
        hp = observation.get("hp", 5) / 5.0
        ammo = observation.get("ammo", 3) / 3.0

        # Normalize position (assuming 50x50 map)
        position = observation.get("position", {"x": 0, "y": 0})
        x = position.get("x", 0) / 50.0
        y = position.get("y", 0) / 50.0

        return [hp, ammo, x, y]

    def _encode_entities(self, entities: List[Dict]) -> List[float]:
        """
        Encode nearby entities.

        Args:
            entities: List of visible entities

        Returns:
            features: Entity position/distance/angle features
        """
        features = []

        for i in range(self.max_entities):
            if i < len(entities):
                entity = entities[i]
                # Relative position
                rel_x = entity.get("relative_x", 0) / 10.0  # Normalize by vision range
                rel_y = entity.get("relative_y", 0) / 10.0

                # Distance (normalized)
                distance = entity.get("distance", 0) / 10.0

                features.extend([rel_x, rel_y, distance])
            else:
                # Padding for missing entities
                features.extend([0.0, 0.0, 0.0])

        return features

    def _encode_sounds(self, sounds: List[Dict]) -> List[float]:
        """
        Encode sound information.

        Args:
            sounds: List of heard sounds

        Returns:
            features: 8-direction encoding
        """
        # 8 directions: N, NE, E, SE, S, SW, W, NW
        direction_features = [0.0] * 8

        direction_map = {
            "north": 0,
            "northeast": 1,
            "east": 2,
            "southeast": 3,
            "south": 4,
            "southwest": 5,
            "west": 6,
            "northwest": 7
        }

        for sound in sounds:
            direction = sound.get("direction", "").lower()
            if direction in direction_map:
                idx = direction_map[direction]
                direction_features[idx] = 1.0

        return direction_features

    def get_feature_dim(self) -> int:
        """Get total feature dimension"""
        return self.feature_dim
