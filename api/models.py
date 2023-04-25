from sqlalchemy import ForeignKey, Integer, Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

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
