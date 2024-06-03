from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api import schemas, database, games, user

router = APIRouter(
    prefix="/games",
    tags=["games"]
)

@router.post("/")
def create_game(
    game: schemas.GameCreate, 
    current_user: Annotated[schemas.User, Depends(user.auth.get_current_user)], 
    db: Session = Depends(database.get_db)
) -> schemas.Game:
    return games.crud.create_game(db, game, current_user)

@router.get("/host")
def get_games_where_host( 
    current_user: Annotated[schemas.User, Depends(user.auth.get_current_user)], 
    db: Session = Depends(database.get_db)
) -> List[schemas.Game]:
    return games.crud.get_games_by_host(db, current_user)

@router.get("/{game_id}")
def get_game_with_id(
    game_id: int,
    current_user: Annotated[schemas.User, Depends(user.auth.get_current_user)],
    db: Session = Depends(database.get_db)
) -> schemas.Game:
    db_game = games.crud.get_game_by_id(db, game_id)
    if db_game.host is not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNuser.authORIZED,
            detail="You are not the host of this game"
        )
    return db_game

@router.post("/{game_id}/add_player")
def add_player(
    game_id: int,
    new_player: schemas.PlayerCreate,
    current_user: Annotated[schemas.User, Depends(user.auth.get_current_user)],
    db: Session = Depends(database.get_db)
) -> schemas.Game:
    game = games.crud.get_game_by_id(db, game_id)
    if game.host is not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNuser.authORIZED,
            detail="You are not the host of this game"
        )
    games.crud.add_player(db, game, new_player.username)
    return game
    
@router.post("/{game_id}/role/{username}")
def set_role(
    game_id: int,
    username: str,
    role: str,
    current_user: Annotated[schemas.User, Depends(user.auth.get_current_user)],
    db: Session = Depends(database.get_db)
) -> None:
    game = games.crud.get_game_by_id(db, game_id)
    if game.host is not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNuser.authORIZED,
            detail="You are not the host of this game"
        )
    games.crud.set_role(db, game, username, role)
    return

@router.post("/{game_id}/team/{username}")
def set_team(
    game_id: int,
    username: str,
    team: str,
    current_user: Annotated[schemas.User, Depends(user.auth.get_current_user)],
    db: Session = Depends(database.get_db)
) -> None:
    game = games.crud.get_game_by_id(db, game_id)
    games.raise_if_not_host(game, current_user)
    games.crud.set_team(db, game, username, team)
    return
    
@router.post("/{game_id}/wakeup")
def wakeup(
    game_id: int,
    current_user: Annotated[schemas.User, Depends(user.auth.get_current_user)],
    db: Session = Depends(database.get_db)
) -> None:
    game = games.crud.get_game_by_id(db, game_id)
    games.raise_if_not_host(game, current_user)
    games.wakeup(db, game)
    return
    
@router.post("/{game_id}/action")
def add_action(
    game_id: int,
    username: str,
    action_name: str,
    player_targets: List[str],
    current_user: Annotated[schemas.User, Depends(user.auth.get_current_user)],
    db: Session = Depends(database.get_db)
) -> None:
    game = games.crud.get_game_by_id(db, game_id)
    games.raise_if_not_host(game, current_user)
    games.crud.add_action(db, game, username, action_name, player_targets)
    return