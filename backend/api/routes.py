"""
Game API routes.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

router = APIRouter(prefix="/game", tags=["game"])


# Request/Response models
class NewGameResponse(BaseModel):
    game_id: str
    observation: Dict[str, Any]
    queue_size: int


class ActionRequest(BaseModel):
    game_id: str
    action: str


class ActionResponse(BaseModel):
    success: bool
    queue_size: int
    message: str


class TickRequest(BaseModel):
    game_id: str


class TickResponse(BaseModel):
    tick: int
    observation: Dict[str, Any]
    events: List[str]
    queue_size: int


class ClearQueueRequest(BaseModel):
    game_id: str


class ClearQueueResponse(BaseModel):
    success: bool
    message: str


class ResumeRequest(BaseModel):
    game_id: str


class ResumeResponse(BaseModel):
    game_id: str
    observation: Dict[str, Any]
    queue_size: int


class ObserveResponse(BaseModel):
    observation: Dict[str, Any]


class WatchResponse(BaseModel):
    game_id: str
    tick: int
    full_map: List[List[str]]
    entities: List[Dict[str, Any]]
    bullets: List[Dict[str, Any]]


class ErrorResponse(BaseModel):
    success: bool
    error: str


# Placeholder endpoints (to be implemented in next stages)

@router.post("/new", response_model=NewGameResponse)
async def create_game():
    """Create a new game."""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.post("/action", response_model=ActionResponse)
async def submit_action(request: ActionRequest):
    """Submit an action to the queue."""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.post("/tick", response_model=TickResponse)
async def execute_tick(request: TickRequest):
    """Execute one game tick."""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.post("/clear_queue", response_model=ClearQueueResponse)
async def clear_queue(request: ClearQueueRequest):
    """Clear action queue (ESC)."""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.post("/resume", response_model=ResumeResponse)
async def resume_game(request: ResumeRequest):
    """Resume a saved game."""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/observe", response_model=ObserveResponse)
async def observe_game(game_id: str):
    """Get current observation."""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/watch", response_model=WatchResponse)
async def watch_game(game_id: str):
    """Watch game in god mode (requires -watch suffix)."""
    raise HTTPException(status_code=501, detail="Not implemented yet")
