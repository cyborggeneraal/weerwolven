from typing import Dict, List, Annotated

from jose import jwt, JWTError
from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api import crud, models, schemas, database, auth, votes, games
from api.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(games.router)
#app.include_router(votes.router)

@app.post("/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(database.get_db)):
    user = auth.authenticate_user(db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )    
    return {"access_token": access_token, "token_type": "bearer"}
        
@app.post("/users")
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)) -> schemas.User:
    db_user = crud.users.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.users.create_user(db=db, user=user)

@app.get("/users/")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)) -> List[schemas.User]:
    users = crud.users.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(database.get_db)) -> schemas.User:
    db_user = crud.users.get_user(db, user_id= user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/")
def read_root(current_user: Annotated[schemas.User, Depends(auth.get_current_user)]) -> str:
    return f"Hello, {current_user.username}"