"""
World state data structures.
Defines EntityState, BulletState, and WorldState.
"""
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Set, Tuple
import uuid

from .constants import INITIAL_HP, INITIAL_AMMO


@dataclass
class EntityState:
    """
    Represents a player or agent in the game.
    """
    entity_id: str
    entity_type: str  # "player" or "agent"
    persona: Optional[str]  # None for player, or "aggressive"/"cautious"/"explorer"

    # Position
    x: int
    y: int

    # Combat stats
    hp: int
    ammo: int
    last_bullet_tick: int  # Tick when last bullet was fired

    # Status
    alive: bool
    won: bool  # True if reached exit

    # Action queue
    action_queue: List[str] = field(default_factory=list)

    # Visited positions for explorer penalty tracking
    visited_positions: Set[Tuple[int, int]] = field(default_factory=set)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dict for database storage."""
        return {
            "entity_id": self.entity_id,
            "entity_type": self.entity_type,
            "persona": self.persona,
            "x": self.x,
            "y": self.y,
            "hp": self.hp,
            "ammo": self.ammo,
            "last_bullet_tick": self.last_bullet_tick,
            "alive": self.alive,
            "won": self.won,
            "action_queue": self.action_queue,
            "visited_positions": list(self.visited_positions)  # Convert set to list
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'EntityState':
        """Deserialize from dict."""
        visited = set(tuple(pos) for pos in data.get("visited_positions", []))
        return EntityState(
            entity_id=data["entity_id"],
            entity_type=data["entity_type"],
            persona=data.get("persona"),
            x=data["x"],
            y=data["y"],
            hp=data["hp"],
            ammo=data["ammo"],
            last_bullet_tick=data["last_bullet_tick"],
            alive=data["alive"],
            won=data["won"],
            action_queue=data.get("action_queue", []),
            visited_positions=visited
        )


@dataclass
class BulletState:
    """
    Represents a bullet in flight.
    """
    shooter_id: str
    x: int
    y: int
    direction: str  # "UP", "DOWN", "LEFT", "RIGHT"
    spawn_tick: int

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dict."""
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'BulletState':
        """Deserialize from dict."""
        return BulletState(**data)


@dataclass
class WorldState:
    """
    Complete game state.
    """
    game_id: str
    tick: int

    # Map data
    map_grid: List[List[str]]  # 50x50 grid
    start_x: int
    start_y: int
    exit_x: int
    exit_y: int

    # Entities
    entities: Dict[str, EntityState]  # entity_id -> EntityState

    # Bullets
    bullets: List[BulletState]

    # Game status
    game_over: bool
    winner_id: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dict for database storage."""
        return {
            "game_id": self.game_id,
            "tick": self.tick,
            "map_grid": self.map_grid,
            "start_x": self.start_x,
            "start_y": self.start_y,
            "exit_x": self.exit_x,
            "exit_y": self.exit_y,
            "entities": {eid: e.to_dict() for eid, e in self.entities.items()},
            "bullets": [b.to_dict() for b in self.bullets],
            "game_over": self.game_over,
            "winner_id": self.winner_id
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'WorldState':
        """Deserialize from dict."""
        entities = {
            eid: EntityState.from_dict(e_data)
            for eid, e_data in data["entities"].items()
        }
        bullets = [BulletState.from_dict(b) for b in data["bullets"]]

        return WorldState(
            game_id=data["game_id"],
            tick=data["tick"],
            map_grid=data["map_grid"],
            start_x=data["start_x"],
            start_y=data["start_y"],
            exit_x=data["exit_x"],
            exit_y=data["exit_y"],
            entities=entities,
            bullets=bullets,
            game_over=data["game_over"],
            winner_id=data.get("winner_id")
        )


def create_entity(
    entity_id: str,
    entity_type: str,
    x: int,
    y: int,
    persona: Optional[str] = None
) -> EntityState:
    """
    Create a new entity with initial stats.

    Args:
        entity_id: Unique ID
        entity_type: "player" or "agent"
        x, y: Starting position
        persona: Optional persona for agents

    Returns:
        EntityState with default stats
    """
    return EntityState(
        entity_id=entity_id,
        entity_type=entity_type,
        persona=persona,
        x=x,
        y=y,
        hp=INITIAL_HP,
        ammo=INITIAL_AMMO,
        last_bullet_tick=0,
        alive=True,
        won=False,
        action_queue=[],
        visited_positions=set()
    )
