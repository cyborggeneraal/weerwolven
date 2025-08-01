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
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=user.auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = user.auth.create_access_token(
        data={"sub": db_user.username}, 
        expires_delta=access_token_expires
    )    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/", response_model=models.User)
def create_user(user_data: models.UserCreate, db: database.SessionDep):
    db_user = user.crud.get_user_by_username(db, username=user_data.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return user.crud.create_user(db=db, user_data=user_data)

@router.get("/", response_model=List[models.User])
def read_users(db: database.SessionDep, skip: int = 0, limit: int = 100):
    users = user.crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{username}", response_model=models.User)
def read_user(username: str, db: database.SessionDep):
    db_user = user.crud.get_user_by_username(db, username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user