from typing import Annotated, List
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from api import database, user, models

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.post("/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: database.SessionDep):
    db_user = user.auth.authenticate_user(db, username=form_data.username, password=form_data.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user.auth.create_access_token(db_user.username)    

@router.post("/")
def create_user(user_data: models.UserCreate, db: database.SessionDep) -> models.UserPublic:
    db_user = user.crud.get_user_by_username(db, username=user_data.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return user.crud.create_user(db=db, user_data=user_data)

@router.get("/")
def read_users(db: database.SessionDep, skip: int = 0, limit: int = 100) -> List[models.UserPublic]:
    users = user.crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{username}")
def read_user(username: str, db: database.SessionDep) -> models.UserPublic:
    db_user = user.crud.get_user_by_username(db, username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user