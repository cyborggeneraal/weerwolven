from typing import List

from sqlalchemy.orm import Session

from api import schemas, models, auth, crud

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
    db_user = crud.users.get_user_by_username(db, username)
    if not db_user:
        db_player = models.Player(username=username, game=game)
    else:
        db_player = models.Player(username=username, game=game, user=db_user)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player