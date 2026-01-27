"""
Concurrent game limiter.
"""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from backend.storage.games_store import count_games
from backend.engine.constants import MAX_CONCURRENT_GAMES


def check_concurrent_limit(db: Session):
    """
    Check if server is at capacity.

    Args:
        db: Database session

    Raises:
        HTTPException: If at capacity (503)
    """
    active_games = count_games(db, game_over=False)

    if active_games >= MAX_CONCURRENT_GAMES:
        raise HTTPException(
            status_code=503,
            detail=f"Server at capacity ({MAX_CONCURRENT_GAMES} concurrent games). Try again later."
        )
