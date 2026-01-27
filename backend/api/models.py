"""
Pydantic models for API requests and responses.
"""
from pydantic import BaseModel
from typing import Dict, Any, List


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
