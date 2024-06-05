from pydantic import BaseModel
from api import schemas

class BaseAction(BaseModel):
    player: schemas.Player
    day: int

class VisionAction(BaseAction):
    target: schemas.Player

class VisionInfo(BaseAction):
    target: schemas.Player
    team: str

class LunchAction(BaseAction):
    target: schemas.Player

class LifePotionAction(BaseAction):
    target: schemas.Player