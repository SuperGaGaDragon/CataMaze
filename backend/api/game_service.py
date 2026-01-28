"""
Game service - business logic for game operations.
"""
from sqlalchemy.orm import Session
from typing import Dict, Any

from backend.engine.state_factory import create_new_state
from backend.engine.engine import GameEngine
from backend.engine.observation import generate_observation
from backend.engine.actions import is_valid_action
from backend.storage.games_store import save_game, load_game, GameStoreError
from backend.storage.log_store import append_logs_batch, LogStoreError
from backend.agents.registry import create_agent


class GameServiceError(Exception):
    """Custom exception for game service operations."""
    pass


def create_new_game(db: Session) -> Dict[str, Any]:
    """Create a new game and return initial state."""
    try:
        world = create_new_state()
        save_game(db, world)
        obs = generate_observation(world, "player")
        return {
            "game_id": world.game_id,
            "observation": obs,
            "queue_size": 0
        }
    except (GameStoreError, Exception) as e:
        raise GameServiceError(f"Failed to create game: {str(e)}")


def queue_action(db: Session, game_id: str, action: str) -> Dict[str, Any]:
    """Queue an action for the player."""
    try:
        if not is_valid_action(action):
            raise GameServiceError(f"Invalid action: {action}")

        world = load_game(db, game_id)
        if not world:
            raise GameServiceError(f"Game not found: {game_id}")

        if world.game_over:
            raise GameServiceError("Game is already over")

        player = world.entities.get("player")
        if not player:
            raise GameServiceError("Player not found")

        if not player.alive:
            raise GameServiceError("Player is dead")

        player.action_queue.append(action)
        save_game(db, world)

        return {
            "success": True,
            "queue_size": len(player.action_queue),
            "message": "Action queued"
        }
    except GameServiceError:
        raise
    except Exception as e:
        raise GameServiceError(f"Failed to queue action: {str(e)}")


def execute_game_tick(db: Session, game_id: str) -> Dict[str, Any]:
    """Execute one game tick."""
    try:
        world = load_game(db, game_id)
        if not world:
            raise GameServiceError(f"Game not found: {game_id}")

        if world.game_over:
            raise GameServiceError("Game is already over")

        # Create AI agent instances for non-player entities
        agents = {}
        for entity_id, entity in world.entities.items():
            if entity.entity_type == "agent" and entity.alive:
                # Create RL agent with persona
                agents[entity_id] = create_agent("rl", entity_id, entity.persona)
                print(f"DEBUG: Created agent {entity_id} with persona {entity.persona}")

        engine = GameEngine(world, agents)
        result = engine.tick()

        save_game(db, world)

        if result["events"]:
            try:
                append_logs_batch(db, game_id, world.tick, result["events"])
            except LogStoreError as e:
                print(f"Warning: Failed to save logs: {e}")

        player_obs = result["observations"].get("player")
        if not player_obs:
            player_obs = generate_observation(world, "player")

        player = world.entities.get("player")
        queue_size = len(player.action_queue) if player else 0

        return {
            "tick": result["tick"],
            "observation": player_obs,
            "events": result["events"],
            "queue_size": queue_size
        }
    except GameServiceError:
        raise
    except Exception as e:
        raise GameServiceError(f"Failed to execute tick: {str(e)}")


def get_game_observation(db: Session, game_id: str) -> Dict[str, Any]:
    """Get current observation for a game."""
    try:
        world = load_game(db, game_id)
        if not world:
            raise GameServiceError(f"Game not found: {game_id}")

        obs = generate_observation(world, "player")
        return {"observation": obs}
    except GameServiceError:
        raise
    except Exception as e:
        raise GameServiceError(f"Failed to get observation: {str(e)}")


def resume_existing_game(db: Session, game_id: str) -> Dict[str, Any]:
    """Resume a game."""
    try:
        world = load_game(db, game_id)
        if not world:
            raise GameServiceError(f"Game not found: {game_id}")

        obs = generate_observation(world, "player")
        player = world.entities.get("player")
        queue_size = len(player.action_queue) if player else 0

        return {
            "game_id": game_id,
            "observation": obs,
            "queue_size": queue_size
        }
    except GameServiceError:
        raise
    except Exception as e:
        raise GameServiceError(f"Failed to resume game: {str(e)}")
