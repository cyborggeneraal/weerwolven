from typing import List
from sqlalchemy import ForeignKey, Integer, Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped

from api.database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    games = relationship("Game", back_populates="host")
    players = relationship("Player", back_populates="user")

class Game(Base):
    __tablename__ = "game"
    
    id = Column(Integer, primary_key=True, index=True)
    host_id = Column(Integer, ForeignKey("user.id"))
    name = Column(String, nullable=True)
    current_day = Column(Integer, default=0)
    
    host = relationship("User", back_populates="games")
    players = relationship("Player", back_populates="game")
    votes = relationship("Vote", back_populates="game")
    
class Player(Base):
    __tablename__ = "player"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    game_id = Column(Integer, ForeignKey("game.id"))
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    rol = Column(String, default="gewone burger")
    team = Column(String, default="burger team")
    
    game = relationship("Game", back_populates="players")
    user = relationship("User", back_populates="players")
    
class Vote(Base):
    __tablename__ = "vote"
    
    id = Column(Integer, primary_key=True, index=True)
    vote_from = Column(String)
    game_id = Column(Integer, ForeignKey("game.id"))
    day = Column(Integer)
    vote_type = Column(Integer)
    # 0 for lynch
    # 1 for mayor
    vote_to = Column(String)
    
    game = relationship("Game", back_populates="votes")

class Action(Base):
    __tablename__ = "action"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("player.id"))
    name = Column(String)

    player = relationship("Player")
    player_targets : Mapped[List[Player]] = relationship(secondary="player_targets_table")

player_targets_table = Table(
    "player_targets_table",
    Base.metadata,
    Column("action_id", ForeignKey("action.id")),
    Column("target_id", ForeignKey("player.id"))
)