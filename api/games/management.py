from typing import List
from api import models, games

from sqlalchemy.orm import Session

def wakeup(db: Session, game: models.Game) -> None:
    db_actions = games.crud.get_actions_wakeup(db, game, game.current_day)

    perform_vision(db, game, db_actions)
    perform_lunch(db, game, db_actions)
    perform_dead_potion(db, game, db_actions)

    perform_healing(db,game,db_actions)
    perform_life_potion(db, game, db_actions)

    games.crud.clean_bodies(db, game)
    game.current_day += 1
    db.commit()
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
            player_targets=[target],
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

def add_life_potion_action(
        db: Session,
        game: models.Game,
        action: games.action_schemas.LifePotionAction
) -> None:
    db_player = games.crud.get_player(db, game, action.player.username)
    db_target = games.crud.get_player(db, game, action.target.username)
    db_action = models.Action(
        name="life_potion",
        player=db_player,
        player_targets=[db_target],
        day=action.day
    )
    db.add(db_action)
    db.commit()

def perform_life_potion(db: Session, game: models.Game, actions: List[models.Action]) -> None:
    life_potion_actions = [action for action in actions if action.name == "life_potion"]
    
    for life_potion_action in life_potion_actions:
        if len(life_potion_action.player_targets) == 1:
            revived = games.crud.revive(db, game, life_potion_action.player_targets[0])
            db_info = models.Info(
                player = life_potion_action.player,
                action = life_potion_action,
                player_targets = [life_potion_action.player_targets[0]],
                success = revived
            )
            db.add(db_info)
        else:
            pass #Raise error

    db.commit()

def add_dead_potion(
        db: Session, 
        game: models.Game, 
        action: games.action_schemas.DeadPotionAction
    ) -> None:
    db_player = games.crud.get_player(db, game, action.player.username)
    db_target = games.crud.get_player(db, game, action.target.username)
    db_action = models.Action(
        name="dead_potion",
        player=db_player,
        player_targets=[db_target],
        day=action.day
    )
    db.add(db_action)
    db.commit()

def perform_dead_potion(db: Session, game: models.Game, actions: List[models.Action]) -> None:
    dead_potion_actions = [action for action in actions if action.name == "dead_potion"]

    for dead_potion_action in dead_potion_actions:
        if len(dead_potion_action.player_targets) == 1:
            games.crud.kill(db, game, dead_potion_action.player_targets[0])
            db_info = models.Info(
                player = dead_potion_action.player,
                action = dead_potion_action,
                player_targets = [dead_potion_action.player_targets[0]]
            )
            db.add(db_info)
        else:
            pass #Raise error

def add_healing(
        db: Session, 
        game: models.Game, 
        action: games.action_schemas.DeadPotionAction
    ) -> None:
    db_player = games.crud.get_player(db, game, action.player.username)
    db_target = games.crud.get_player(db, game, action.target.username)
    db_action = models.Action(
        name="healing",
        player=db_player,
        player_targets=[db_target],
        day=action.day
    )
    db.add(db_action)
    db.commit()

def perform_healing(db: Session, game: models.Game, actions: List[models.Action]) -> None:
    healing_actions = [action for action in actions if action.name == "healing"]
    
    for healing_action in healing_actions:
        if len(healing_action.player_targets) == 1:
            revived = games.crud.revive(db, game, healing_action.player_targets[0])
            db_info = models.Info(
                player = healing_action.player,
                action = healing_action,
                player_targets = [healing_action.player_targets[0]],
                success = revived
            )
            db.add(db_info)
        else:
            pass #Raise error

    db.commit()

def add_sniff(
    db: Session, 
    game: models.Game, 
    action: games.action_schemas.SniffAction
) -> None:
    db_player = games.crud.get_player(db, game, action.player.username)
    db_targets = [
        games.crud.get_player(db, game, action.target1.username),
        games.crud.get_player(db, game, action.target2.username),
        games.crud.get_player(db, game, action.target3.username)
    ]
    db_action = models.Action(
        name="sniff", 
        player=db_player, 
        player_targets=db_targets,
        day=action.day
    )
    db.add(db_action)
    db.commit()

def perform_sniff(db: Session, game: models.Game, actions: List[models.Action]) -> None:
    sniff_actions = [action for action in actions if action.name == "seer_vision"]
    for sniff_action in sniff_actions:
        if len(sniff_action.player_targets) != 3:
            continue
        new_info = models.Info(
            player=sniff_action.player,
            action=sniff_action,
            player_targets=sniff_action.player_targets,
            success=any(target.team == "weerwolf team" for target in sniff_action.player_targets)
        )
        db.add(new_info)
    db.commit()
    return

