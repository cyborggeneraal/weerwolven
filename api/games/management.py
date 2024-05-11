from typing import List
from api import models, games

from sqlalchemy.orm import Session

def wakeup(db: Session, game: models.Game) -> None:
    db_actions = games.crud.get_actions_wakeup(db, game, game.current_day+1)

    perform_lunch(db, game, db_actions)
    perform_visioen(db, game, db_actions)

    games.crud.clean_bodies(db, game)
    return

def perform_visioen(db: Session, game: models.Game, actions: List[models.Action]) -> None:
    visioen_actions = [action for action in actions if action.name == "ziener_visioen"]
    for visioen_action in visioen_actions:
        if len(visioen_action.player_targets) != 1:
            continue
        target = visioen_action.player_targets[0]
        new_info = games.crud.see_team(db, game, visioen_action.player, [target])
        db.add(new_info)
    db.commit()
    return

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