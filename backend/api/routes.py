"""
Game API routes.
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from storage.db import get_db
from storage.games_store import load_game, save_game
from api.models import *
from api.game_service import (
    create_new_game,
    queue_action,
    execute_game_tick,
    get_game_observation,
    resume_existing_game,
    GameServiceError
)

router = APIRouter(prefix="/game", tags=["game"])


@router.post("/new", response_model=NewGameResponse)
async def create_game(db: Session = Depends(get_db)):
    """Create a new game."""
    try:
        return create_new_game(db)
    except GameServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/action", response_model=ActionResponse)
async def submit_action(request: ActionRequest, db: Session = Depends(get_db)):
    """Submit an action to the queue."""
    try:
        return queue_action(db, request.game_id, request.action)
    except GameServiceError as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/tick", response_model=TickResponse)
async def execute_tick(request: TickRequest, db: Session = Depends(get_db)):
    """Execute one game tick."""
    try:
        return execute_game_tick(db, request.game_id)
    except GameServiceError as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/clear_queue", response_model=ClearQueueResponse)
async def clear_queue(request: ClearQueueRequest, db: Session = Depends(get_db)):
    """Clear action queue (ESC)."""
    try:
        world = load_game(db, request.game_id)
        if not world:
            raise HTTPException(status_code=404, detail="Game not found")

        player = world.entities.get("player")
        if player:
            player.action_queue.clear()
            save_game(db, world)

        return {"success": True, "message": "Queue cleared"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/resume", response_model=ResumeResponse)
async def resume_game(request: ResumeRequest, db: Session = Depends(get_db)):
    """Resume a saved game."""
    try:
        return resume_existing_game(db, request.game_id)
    except GameServiceError as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/observe", response_model=ObserveResponse)
async def observe_game(game_id: str, db: Session = Depends(get_db)):
    """Get current observation."""
    try:
        return get_game_observation(db, game_id)
    except GameServiceError as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/watch", response_model=WatchResponse)
async def watch_game(game_id: str, db: Session = Depends(get_db)):
    """Watch game in god mode (requires -watch suffix)."""
    if not game_id.endswith("-watch"):
        raise HTTPException(
            status_code=403,
            detail="Watch mode requires game_id to end with '-watch'"
        )

    actual_game_id = game_id[:-6]

    try:
        world = load_game(db, actual_game_id)
        if not world:
            raise HTTPException(status_code=404, detail="Game not found")

        entities = [
            {
                "entity_id": e.entity_id,
                "entity_type": e.entity_type,
                "persona": e.persona,
                "position": {"x": e.x, "y": e.y},
                "hp": e.hp,
                "ammo": e.ammo,
                "alive": e.alive,
                "won": e.won
            }
            for e in world.entities.values()
        ]

        bullets = [b.to_dict() for b in world.bullets]

        return {
            "game_id": actual_game_id,
            "tick": world.tick,
            "full_map": world.map_grid,
            "entities": entities,
            "bullets": bullets
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
