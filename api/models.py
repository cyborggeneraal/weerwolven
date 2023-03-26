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
    
    host = relationship("User", back_populates="games")
    players = relationship("Player", back_populates="game")
    
class Player(Base):
    __tablename__ = "player"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    is_fake = Column(Boolean, default=True)
    game_id = Column(Integer, ForeignKey("game.id"))
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    
    game = relationship("Game", back_populates="players")
    user = relationship("User", back_populates="players")
