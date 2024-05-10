from fastapi import HTTPException, status
from api.games.routes import router
from api.games import crud
from api.games.management import *

from api import models

def raise_if_not_host(game: models.Game, user: models.User) -> None:
    if game.host is not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not the host of this game"
        )
    return