from typing import List

from sqlalchemy.orm import Session

from api import schemas, models, auth

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username = user.username, hashed_password = hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_game(db: Session, game: schemas.GameCreate, host: schemas.User) -> models.Game:
    db_game = models.Game(host=host, name=game.name)
    for player in game.players:
        if isinstance(player, str):
            db_game.players.add(player)
        else:
            db_game.players.add(get_user_by_username(player.username))
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

def get_games_by_host(db: Session, host: schemas.User) -> List[models.Game]:
    return db.query(models.Game).filter(models.Game.host == host).all()

def get_game_by_id(db: Session, game_id: int) -> models.Game:
    return db.query(models.Game).filter(models.Game.id == game_id).first()

def add_player(db: Session, game: schemas.Game, username: str) -> models.Player:
    db_user = get_user_by_username(db, username)
    if not db_user:
        db_player = models.Player(username=username, game=game, is_fake=True)
    else:
        db_player = models.Player(username=username, game=game, user=db_user, is_fake=False)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player