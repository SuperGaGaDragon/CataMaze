"""
Game state storage operations.
CRUD operations for game states.
"""
import json
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List, Dict, Any

from backend.storage.models import Game
from backend.engine.state import WorldState


class GameStoreError(Exception):
    """Custom exception for game store operations."""
    pass


def save_game(db: Session, world: WorldState) -> Game:
    """
    Save or update game state.

    Args:
        db: Database session
        world: World state to save

    Returns:
        Saved Game model

    Raises:
        GameStoreError: If save fails
    """
    try:
        # Serialize world state
        world_state_json = json.dumps(world.to_dict())

        # Check if game exists
        existing_game = db.query(Game).filter(Game.game_id == world.game_id).first()

        if existing_game:
            # Update existing game
            existing_game.tick = world.tick
            existing_game.world_state = world_state_json
            existing_game.game_over = world.game_over
            existing_game.winner_id = world.winner_id
            db.commit()
            db.refresh(existing_game)
            return existing_game
        else:
            # Create new game
            new_game = Game(
                game_id=world.game_id,
                tick=world.tick,
                world_state=world_state_json,
                game_over=world.game_over,
                winner_id=world.winner_id
            )
            db.add(new_game)
            db.commit()
            db.refresh(new_game)
            return new_game

    except SQLAlchemyError as e:
        db.rollback()
        raise GameStoreError(f"Failed to save game {world.game_id}: {str(e)}")
    except Exception as e:
        db.rollback()
        raise GameStoreError(f"Unexpected error saving game {world.game_id}: {str(e)}")


def load_game(db: Session, game_id: str) -> Optional[WorldState]:
    """
    Load game state from database.

    Args:
        db: Database session
        game_id: Game ID to load

    Returns:
        WorldState if found, None otherwise

    Raises:
        GameStoreError: If load fails
    """
    try:
        game = db.query(Game).filter(Game.game_id == game_id).first()

        if not game:
            return None

        # Deserialize world state
        world_dict = json.loads(game.world_state)
        return WorldState.from_dict(world_dict)

    except json.JSONDecodeError as e:
        raise GameStoreError(f"Failed to parse game state for {game_id}: {str(e)}")
    except Exception as e:
        raise GameStoreError(f"Failed to load game {game_id}: {str(e)}")


def delete_game(db: Session, game_id: str) -> bool:
    """
    Delete a game from database.

    Args:
        db: Database session
        game_id: Game ID to delete

    Returns:
        True if deleted, False if not found

    Raises:
        GameStoreError: If delete fails
    """
    try:
        game = db.query(Game).filter(Game.game_id == game_id).first()

        if not game:
            return False

        db.delete(game)
        db.commit()
        return True

    except SQLAlchemyError as e:
        db.rollback()
        raise GameStoreError(f"Failed to delete game {game_id}: {str(e)}")


def list_games(db: Session, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
    """
    List games with pagination.

    Args:
        db: Database session
        limit: Maximum number of games to return
        offset: Number of games to skip

    Returns:
        List of game summaries

    Raises:
        GameStoreError: If query fails
    """
    try:
        games = db.query(Game).offset(offset).limit(limit).all()

        return [
            {
                "game_id": game.game_id,
                "tick": game.tick,
                "game_over": game.game_over,
                "winner_id": game.winner_id,
                "created_at": game.created_at.isoformat() if game.created_at else None,
                "updated_at": game.updated_at.isoformat() if game.updated_at else None
            }
            for game in games
        ]

    except SQLAlchemyError as e:
        raise GameStoreError(f"Failed to list games: {str(e)}")


def count_games(db: Session, game_over: Optional[bool] = None) -> int:
    """
    Count games, optionally filtered by game_over status.

    Args:
        db: Database session
        game_over: Optional filter for game_over status

    Returns:
        Number of games

    Raises:
        GameStoreError: If query fails
    """
    try:
        query = db.query(Game)

        if game_over is not None:
            query = query.filter(Game.game_over == game_over)

        return query.count()

    except SQLAlchemyError as e:
        raise GameStoreError(f"Failed to count games: {str(e)}")
