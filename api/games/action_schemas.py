from pydantic import BaseModel
from api import schemas

class BaseAction(BaseModel):
    day: int

class VisionAction(BaseAction):
    target: schemas.Player