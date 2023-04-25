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

class PlayerBase(BaseModel):
    username: str

class Player(PlayerBase):
    is_fake: bool = True
    
    @classmethod
    def from_orm(cls, obj):
        obj_schema = super().from_orm(obj)
        obj_schema.is_fake = obj.user_id == None  
        return obj_schema
    
    class Config:
        orm_mode = True
        
class PlayerCreate(PlayerBase):
    
    class Config:
        orm_mode = True

class GameBase(BaseModel):
    pass

class GameGet(GameBase):
    id: int    

class GameCreate(GameBase):
    players: List[str] = []
    name: str

class Game(GameBase):
    id: int
    host: User
    players: List[Player]
    name: str
    
    class Config:
        orm_mode = True