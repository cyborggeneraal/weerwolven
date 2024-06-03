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
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not the host of this game"
        )
    return db_game

@router.get("/{game_id}/players")
def get_players(
    game_id: int,
    current_user: Annotated[schemas.User, Depends(user.auth.get_current_user)],
    db: Session = Depends(database.get_db)
) -> List[schemas.Player]:
    db_game = games.crud.get_game_by_id(db, game_id)
    games.raise_if_not_host(db_game, current_user)
    return games.crud.get_players(db, db_game)

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
            status_code=status.HTTP_401_UNAUTHORIZED,
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
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not the host of this game"
        )
    games.crud.set_role(db, game, username, role)
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
    
@router.post("/{game_id}/action/vision")
def add_vision_action(
    game_id: int,
    action: games.action_schemas.VisionAction,
    current_user: Annotated[schemas.User, Depends(user.auth.get_current_user)],
    db: Session = Depends(database.get_db)
) -> None:
    game = games.crud.get_game_by_id(db, game_id)
    games.raise_if_not_host(game, current_user)
    games.add_vision_action(db, game, action)
    return

@router.post("/{game_id}/info/vision")
def get_vision_info(
    game_id: int,
    player: schemas.Player,
    current_user: Annotated[schemas.User, Depends(user.auth.get_current_user)],
    db: Session = Depends(database.get_db)
) -> List[games.action_schemas.VisionInfo]:
    db_game = games.crud.get_game_by_id(db, game_id)
    infos = games.crud.get_infos(db, db_game, player.username)
    return [games.action_schemas.VisionInfo(
        player=info.player,
        day=info.day,
        target=info.player_targets[0],
        team=info.team_targets[0]
    ) for info in infos
    if info.action.name == "seer_vision"]

@router.post("/{game_id}/action/lunch")
def add_lunch_action(
    game_id: int,
    action: games.action_schemas.LunchAction,
    current_user: Annotated[schemas.User, Depends(user.auth.get_current_user)],
    db: Session = Depends(database.get_db)
) -> None:
    db_game = games.crud.get_game_by_id(db, game_id)
    games.raise_if_not_host(db_game, current_user)
    games.add_lunch_action(db, db_game, action)
    return