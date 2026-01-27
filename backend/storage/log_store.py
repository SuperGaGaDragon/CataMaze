"""
Event log storage operations.
"""
import json
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List, Dict, Any
from backend.storage.models import Log


class LogStoreError(Exception):
    """Custom exception for log store operations."""
    pass


def append_log(
    db: Session,
    game_id: str,
    tick: int,
    event_type: str,
    message: str,
    entity_id: Optional[str] = None,
    extra_data: Optional[Dict[str, Any]] = None
) -> Log:
    """Append a log entry."""
    try:
        extra_data_json = json.dumps(extra_data) if extra_data else None
        log = Log(
            game_id=game_id,
            tick=tick,
            entity_id=entity_id,
            event_type=event_type,
            message=message,
            extra_data=extra_data_json
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log
    except SQLAlchemyError as e:
        db.rollback()
        raise LogStoreError(f"Failed to append log: {str(e)}")


def append_logs_batch(
    db: Session,
    game_id: str,
    tick: int,
    events: List[str],
    event_type: str = "game_event"
) -> int:
    """Append multiple log entries in batch."""
    try:
        logs = [
            Log(
                game_id=game_id,
                tick=tick,
                event_type=event_type,
                message=message,
                entity_id=None,
                extra_data=None
            )
            for message in events
        ]
        db.add_all(logs)
        db.commit()
        return len(logs)
    except SQLAlchemyError as e:
        db.rollback()
        raise LogStoreError(f"Failed to append batch logs: {str(e)}")


def read_logs(
    db: Session,
    game_id: str,
    limit: int = 100,
    offset: int = 0,
    entity_id: Optional[str] = None,
    event_type: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Read logs for a game with optional filters."""
    try:
        query = db.query(Log).filter(Log.game_id == game_id)
        if entity_id:
            query = query.filter(Log.entity_id == entity_id)
        if event_type:
            query = query.filter(Log.event_type == event_type)
        logs = query.order_by(Log.tick, Log.id).offset(offset).limit(limit).all()

        return [
            {
                "id": log.id,
                "game_id": log.game_id,
                "tick": log.tick,
                "entity_id": log.entity_id,
                "event_type": log.event_type,
                "message": log.message,
                "extra_data": json.loads(log.extra_data) if log.extra_data else None,
                "created_at": log.created_at.isoformat() if log.created_at else None
            }
            for log in logs
        ]
    except (SQLAlchemyError, json.JSONDecodeError) as e:
        raise LogStoreError(f"Failed to read logs: {str(e)}")


def count_logs(
    db: Session,
    game_id: str,
    entity_id: Optional[str] = None,
    event_type: Optional[str] = None
) -> int:
    """Count logs for a game with optional filters."""
    try:
        query = db.query(Log).filter(Log.game_id == game_id)
        if entity_id:
            query = query.filter(Log.entity_id == entity_id)
        if event_type:
            query = query.filter(Log.event_type == event_type)
        return query.count()
    except SQLAlchemyError as e:
        raise LogStoreError(f"Failed to count logs: {str(e)}")


def delete_logs(db: Session, game_id: str) -> int:
    """Delete all logs for a game."""
    try:
        count = db.query(Log).filter(Log.game_id == game_id).delete()
        db.commit()
        return count
    except SQLAlchemyError as e:
        db.rollback()
        raise LogStoreError(f"Failed to delete logs: {str(e)}")
