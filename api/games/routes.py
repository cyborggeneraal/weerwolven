from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from api import models, database, games, user

router = APIRouter(
    prefix="/games",
    tags=["games"]
)

@router.post("/")
def create_game(
    game: models.GameCreate, 
    current_user: Annotated[models.User, Depends(user.auth.get_current_user)], 
    db: database.SessionDep
) -> models.GamePublic:
    return games.crud.create_game(db, game, current_user)

@router.get("/host")
def get_games_where_host( 
    current_user: Annotated[models.User, Depends(user.auth.get_current_user)], 
    db: database.SessionDep
) -> List[models.GamePublic]:
    return games.crud.get_games_by_host(db, current_user)

@router.get("/{game_id}")
def get_game_with_id(
    game_id: int,
    current_user: Annotated[models.User, Depends(user.auth.get_current_user)],
    db: database.SessionDep
) -> models.GamePublic | None:
    db_game = games.crud.get_game_by_id(db, game_id)
    if not db_game: return None
    if db_game.host is not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not the host of this game"
        )
    return db_game

#@router.get("/{game_id}/players", response_model=List[schemas.Player])
#def get_players(
#    game_id: int,
#    current_user: Annotated[models.User, Depends(user.auth.get_current_user)],
#    db: database.SessionDep
#):
#    db_game = games.crud.get_game_by_id(db, game_id)
#    games.raise_if_not_host(db_game, current_user)
#    return games.crud.get_players(db, db_game)

#@router.get("/{game_id}/player/{playername}", response_model=schemas.Player)
#def get_player(
#    game_id: int,
#    playername: str,
#    current_user: Annotated[models.User, Depends(user.auth.get_current_user)],
#    db: database.SessionDep
#):
#    db_game = games.crud.get_game_by_id(db, game_id)
#    games.raise_if_not_host(db_game, current_user)
#    games.crud.get_player(db, db_game, playername)
#    return

#@router.post("/{game_id}/add_player", response_model=models.Game)
#def add_player(
#    game_id: int,
#    new_player: schemas.PlayerCreate,
#    current_user: Annotated[models.User, Depends(user.auth.get_current_user)],
#    db: database.SessionDep
#):
#    game = games.crud.get_game_by_id(db, game_id)
#    if game.host is not current_user:
#        raise HTTPException(
#            status_code=status.HTTP_401_UNAUTHORIZED,
#            detail="You are not the host of this game"
#        )
#    games.crud.add_player(db, game, new_player.username)
#    return game
    
@router.post("/{game_id}/role/{username}")
def set_role(
    game_id: int,
    username: str,
    role: str,
    current_user: Annotated[models.User, Depends(user.auth.get_current_user)],
    db: database.SessionDep
):
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
    current_user: Annotated[models.User, Depends(user.auth.get_current_user)],
    db: database.SessionDep
):
    game = games.crud.get_game_by_id(db, game_id)
    games.raise_if_not_host(game, current_user)
    games.wakeup(db, game)
    return
    
@router.post("/{game_id}/action/vision")
def add_vision_action(
    game_id: int,
    action: games.action_schemas.VisionAction,
    current_user: Annotated[models.User, Depends(user.auth.get_current_user)],
    db: database.SessionDep
):
    game = games.crud.get_game_by_id(db, game_id)
    games.raise_if_not_host(game, current_user)
    games.add_vision_action(db, game, action)
    return

#@router.post("/{game_id}/info/vision", response_model=List[games.action_schemas.VisionInfo])
#def get_vision_info(
#    game_id: int,
#    player: schemas.PlayerGet,
#    current_user: Annotated[models.User, Depends(user.auth.get_current_user)],
#    db: database.SessionDep
#):
#    db_game = games.crud.get_game_by_id(db, game_id)
#    infos = games.crud.get_infos(db, db_game, player.username)
#    return [games.action_schemas.VisionInfo(
#        player=info.player,
#        day=info.day,
#        target=info.player_targets[0],
#        team=info.team_targets[0]
#    ) for info in infos
#    if info.action.name == "seer_vision"]

@router.post("/{game_id}/action/lunch")
def add_lunch_action(
    game_id: int,
    action: games.action_schemas.LunchAction,
    current_user: Annotated[models.User, Depends(user.auth.get_current_user)],
    db: database.SessionDep
):
    db_game = games.crud.get_game_by_id(db, game_id)
    games.raise_if_not_host(db_game, current_user)
    games.add_lunch_action(db, db_game, action)
    return

@router.post("/{game_id}/action/life_potion")
def add_life_potion_action(
    game_id: int,
    action: games.action_schemas.LifePotionAction,
    current_user: Annotated[models.User, Depends(user.auth.get_current_user)],
    db: database.SessionDep
):
    db_game = games.crud.get_game_by_id(db, game_id)
    games.raise_if_not_host(db_game, current_user)
    games.add_life_potion_action(db, db_game, action)
    return

@router.post("/{game_id}/action/dead_potion")
def add_dead_potion_action(
    game_id: int,
    action: games.action_schemas.DeadPotionAction,
    current_user: Annotated[models.User, Depends(user.auth.get_current_user)],
    db: database.SessionDep
):
    db_game = games.crud.get_game_by_id(db, game_id)
    games.raise_if_not_host(db_game,current_user)
    games.add_dead_potion(db, db_game, action)
    return

@router.post("/{game_id}/action/healing")
def add_healing_action(
    game_id: int,
    action: games.action_schemas.HealingAction,
    current_user: Annotated[models.User, Depends(user.auth.get_current_user)],
    db: database.SessionDep
):
    db_game = games.crud.get_game_by_id(db, game_id)
    games.raise_if_not_host(db_game,current_user)
    games.add_healing(db, db_game, action)
    return

@router.post("/{game_id}/action/sniff")
def add_sniff_action(
    game_id: int,
    action: games.action_schemas.SniffAction,
    current_user: Annotated[models.User, Depends(user.auth.get_current_user)],
    db: database.SessionDep
):
    db_game = games.crud.get_game_by_id(db, game_id)
    games.raise_if_not_host(db_game,current_user)
    games.add_sniff(db, db_game, action)
    return