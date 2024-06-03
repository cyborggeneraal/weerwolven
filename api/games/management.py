from typing import List
from api import models, games

from sqlalchemy.orm import Session

def wakeup(db: Session, game: models.Game) -> None:
    db_actions = games.crud.get_actions_wakeup(db, game, game.current_day)

    perform_lunch(db, game, db_actions)
    perform_vision(db, game, db_actions)

    games.crud.clean_bodies(db, game)
    return

def add_vision_action(
    db: Session, 
    game: models.Game, 
    action: games.action_schemas.VisionAction
) -> None:
    db_player = games.crud.get_player(db, game, action.player.username)
    db_target = games.crud.get_player(db, game, action.target.username)
    db_action = models.Action(
        name="seer_vision", 
        player=db_player, 
        player_targets=[db_target],
        day=action.day
    )
    db.add(db_action)
    db.commit()

def perform_vision(db: Session, game: models.Game, actions: List[models.Action]) -> None:
    vision_actions = [action for action in actions if action.name == "seer_vision"]
    for vision_action in vision_actions:
        if len(vision_action.player_targets) != 1:
            continue
        target = vision_action.player_targets[0]
        new_info = models.Info(
            player=vision_action.player,
            action=vision_action,
            day=game.current_day,
            team_targets=[target.team]
        )
        db.add(new_info)
    db.commit()
    return

def add_lunch_action(
    db: Session, 
    game: models.Game, 
    action: games.action_schemas.LunchAction
) -> None:
    db_player = games.crud.get_player(db, game, action.player.username)
    db_target = games.crud.get_player(db, game, action.target.username)
    db_action = models.Action(
        name="weerwolf_lunch",
        player=db_player,
        player_targets=[db_target],
        day=action.day
    )
    db.add(db_action)
    db.commit()

def perform_lunch(db: Session, game: models.Game, actions: List[models.Action]) -> None:
    lunch_actions = [action for action in actions if action.name == "weerwolf_lunch"]
    if len(lunch_actions) == 0:
        return
    
    # lunch action
    lunch_action = lunch_actions[0]
    if len(lunch_action.player_targets) != 1:
        return
    target = lunch_action.player_targets[0]
    games.crud.kill(db, game, target)