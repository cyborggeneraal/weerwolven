from pydantic import BaseModel
from api import schemas

class BaseAction(BaseModel):
    player: schemas.Player
    day: int

class VisionAction(BaseAction):
    target: schemas.Player
