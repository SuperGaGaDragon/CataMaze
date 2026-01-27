"""
Database models for Game and Log tables.
"""
from sqlalchemy import Column, String, Integer, Text, DateTime, Boolean
from sqlalchemy.sql import func
from backend.storage.db import Base


class Game(Base):
    """
    Game state table.
    Stores world state as JSON.
    """
    __tablename__ = "games"

    game_id = Column(String(36), primary_key=True, index=True)
    tick = Column(Integer, nullable=False, default=0)
    world_state = Column(Text, nullable=False)  # JSON string
    game_over = Column(Boolean, default=False, index=True)
    winner_id = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    def __repr__(self):
        return f"<Game(game_id={self.game_id}, tick={self.tick}, game_over={self.game_over})>"


class Log(Base):
    """
    Event log table.
    Stores game events and agent reward/penalty logs.
    """
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(String(36), index=True, nullable=False)
    tick = Column(Integer, nullable=False, index=True)
    entity_id = Column(String(50), index=True, nullable=True)  # Optional for agent logs
    event_type = Column(String(50), nullable=False)  # "game_event", "reward", "penalty"
    message = Column(Text, nullable=False)
    extra_data = Column(Text, nullable=True)  # JSON string for additional data
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Log(id={self.id}, game_id={self.game_id}, tick={self.tick}, type={self.event_type})>"
