from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Any
from api import models

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):

    class Config:
        orm_mode = True

class Player(BaseModel):
    username: str
    is_fake: bool
    
    class Config:
        orm_mode = True    

class GameBase(BaseModel):
    pass

class GameGet(GameBase):
    id: int    

class GameCreate(GameBase):
    players: List[Player] | None = []
    name: str

class Game(GameBase):
    id: int
    host: User
    players: List[Player]
    name: str
    
    class Config:
        orm_mode = True