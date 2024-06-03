from typing import List

from sqlalchemy.orm import Session

from api import schemas, models, user

ALIVE = "alive"
KILLED = "killed"
DEAD = "dead"

def create_game(db: Session, game: schemas.GameCreate, host: schemas.User) -> models.Game:
    db_game = models.Game(host=host, name=game.name)
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    schema_game = get_game_by_id(db, db_game.id)
    for player_username in game.players:
        add_player(db, schema_game, player_username)
    
    return db_game

def get_games_by_host(db: Session, host: schemas.User) -> List[models.Game]:
    return db.query(models.Game).filter(models.Game.host == host).all()

def get_game_by_id(db: Session, game_id: int) -> models.Game:
    return db.query(models.Game).filter(models.Game.id == game_id).first()

def add_player(db: Session, game: schemas.Game, username: str) -> models.Player:
    db_user = user.crud.get_user_by_username(db, username)
    if not db_user:
        db_player = models.Player(username=username, game=game)
    else:
        db_player = models.Player(username=username, game=game, user=db_user)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

def get_player(db: Session, game: schemas.Game, username: str) -> models.Player:
    return db.query(models.Player).filter(models.Player.game_id == game.id).filter(models.Player.username == username).first()

def get_players(db: Session, game: models.Game) -> List[models.Player]:
    return db.query(models.Player).filter(models.Player.game == game).all()

def set_role(db: Session, game: schemas.Game, username: str, role: str) -> None:
    db_player: models.Player = get_player(db, game, username)
    db_player.rol = role
    db.commit()
    return

def set_team(db: Session, game: schemas.Game, username: str, team: str) -> None:
    db_player = get_player(db, game, username)
    db_player.team = team
    db.commit()
    return

def add_action(db: Session, game: models.Game, username: str, action_name: str, player_targets: List[str]) -> None:
    db_player = get_player(db, game, username)
    db_player_targets = list(map(lambda _username : get_player(db, game, _username), player_targets))
    db_action = models.Action(player=db_player, name=action_name, player_targets=db_player_targets, day=game.current_day+1)
    db.add(db_action)
    db.commit()
    return

def get_actions_wakeup(db: Session, game: models.Game, day: int) -> List[models.Action]:
    return db.query(models.Action).filter(models.Action.player.has(game=game)).filter(models.Action.day == day).all()

def kill(db: Session, game: models.Game, player: models.Player) -> None:
    player.health_status = KILLED
    db.commit()
    return

def clean_bodies(db: Session, game: models.Game) -> None:
    db_players = db.query(models.Player).filter(models.Player.game == game).filter(models.Player.health_status == KILLED).all()
    for db_player in db_players:
        db_player.health_status = DEAD
    db.commit()
    return

def see_team(db: Session, game: models.Game, player: models.Player, target_players: List[models.Player]) -> models.Info:
    return models.Info(
        player = player,
            name = "ziener_visioen",
            day = game.current_day,
            player_targets = target_players,
            team_targets = [target_player.team for target_player in target_players]
    )
