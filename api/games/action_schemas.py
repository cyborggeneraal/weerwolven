from pydantic import BaseModel
from api import schemas

class BaseAction(BaseModel):
    player: schemas.PlayerGet
    day: int

class VisionAction(BaseAction):
    target: schemas.PlayerGet

class VisionInfo(VisionAction):
    team: str

class LunchAction(BaseAction):
    target: schemas.PlayerGet

class LifePotionAction(BaseAction):
    target: schemas.PlayerGet

class DeadPotionAction(BaseAction):
    target: schemas.PlayerGet

class HealingAction(BaseAction):
    target: schemas.PlayerGet

class SniffAction(BaseAction):
    target1: schemas.PlayerGet
    target2: schemas.PlayerGet
    target3: schemas.PlayerGet