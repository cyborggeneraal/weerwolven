from __future__ import annotations
from typing import List
from sqlalchemy import ForeignKey, Integer, Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column

from api.database import Base

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column()
    
    games: Mapped[List[Game]] = relationship(back_populates="host")
    players: Mapped[List[Player]] = relationship(back_populates="user")

class Game(Base):
    __tablename__ = "game"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    host_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    name: Mapped[str] = mapped_column(nullable=True)
    current_day: Mapped[int] = mapped_column(default=0)
    
    host: Mapped[User] = relationship(back_populates="games")
    players: Mapped[List[Player]] = relationship(back_populates="game")
    votes: Mapped[Vote] = relationship(back_populates="game")
    
class Player(Base):
    __tablename__ = "player"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column()
    game_id: Mapped[int] = mapped_column(ForeignKey("game.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    role: Mapped[str] = mapped_column(default="gewone burger")
    team: Mapped[str] = mapped_column(default="burger team")
    health_status: Mapped[str] = mapped_column(default="alive")
    
    game: Mapped[Game] = relationship(back_populates="players")
    user: Mapped[User] = relationship(back_populates="players")
    
class Vote(Base):
    __tablename__ = "vote"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    vote_from: Mapped[str] = mapped_column()
    game_id: Mapped[int] = mapped_column(ForeignKey("game.id"))
    day: Mapped[int] = mapped_column()
    vote_type: Mapped[int] = mapped_column()
    # 0 for lynch
    # 1 for mayor
    vote_to: Mapped[str] = mapped_column()
    
    game: Mapped[Game] = relationship(back_populates="votes")

class Action(Base):
    __tablename__ = "action"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("player.id"))
    name: Mapped[str] = mapped_column()
    day: Mapped[int] = mapped_column()

    player: Mapped[Player] = relationship()
    player_targets : Mapped[List[Player]] = relationship(secondary="player_targets_table")

player_targets_table = Table(
    "player_targets_table",
    Base.metadata,
    Column("action_id", ForeignKey("action.id")),
    Column("target_id", ForeignKey("player.id"))
)

class Info(Base):
    __tablename__ = "info"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    player: Mapped[Player] = relationship()
    name: Mapped[str] = mapped_column()
    day: Mapped[int] = mapped_column()
    player_targets: Mapped[List[Player]] = relationship(secondary="player_targets_info_table")
    team_targets: Mapped[List[str]] = relationship(secondary="player_targets")

player_targets_info_table = Table(
    "player_targets_info_table",
    Base.metadata,
    Column("info_id", ForeignKey("action.id")),
    Column("target_id", ForeignKey("player.id"))
)

team_targets_info_table = Table(
    "team_targets_info_table",
    Base.metadata,
    Column("info_id", ForeignKey("info.id")),
    Column("team", String)
)