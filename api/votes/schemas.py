from pydantic import BaseModel
from enum import Enum

class VoteType(Enum):
    LYNCH = 0
    MAYOR = 1

class VoteBase(BaseModel):
    vote_from: str
    vote_to: str
    vote_type: VoteType

class VoteCreate(VoteBase):
    pass

class Vote(VoteBase):
    day: int
    
    class Config:
        orm_mode = True