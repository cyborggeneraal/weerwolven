from typing import List

from api import models, schemas, user
from sqlmodel import Session, select

def get_user(db: Session, user_id: int) -> models.User | None:
    statement = select(models.User).where(models.User.id == user_id)
    db_user = db.exec(statement).first()
    return db_user

def get_user_by_username(db: Session, username: str) -> models.User | None:
    statement = select(models.User).where(models.User.username == username)
    db_user = db.exec(statement).first()
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    statement = select(models.User).offset(skip).limit(limit)
    db_users = db.exec(statement).all()
    return db_users

def create_user(db: Session, user_data: schemas.UserCreate):
    hashed_password = user.auth.get_password_hash(user_data.password)
    db_user = models.User(username = user_data.username, hashed_password = hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
