from typing import Dict, List, Annotated

from jose import jwt, JWTError
from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api import crud, models, schemas, database, auth, votes
from api.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(votes.router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
        
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(database.get_db)) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = auth.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.users.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

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

@app.post("/games/")
def create_game(
    game: schemas.GameCreate, 
    current_user: Annotated[schemas.User, Depends(get_current_user)], 
    db: Session = Depends(database.get_db)
) -> schemas.Game:
    return crud.games.create_game(db, game, current_user)

@app.get("/games/host")
def get_games_where_host( 
    current_user: Annotated[schemas.User, Depends(get_current_user)], 
    db: Session = Depends(database.get_db)
) -> List[schemas.Game]:
    return crud.games.get_games_by_host(db, current_user)

@app.get("/games/{game_id}")
def get_game_with_id(
    game_id: int,
    current_user: Annotated[schemas.User, Depends(get_current_user)],
    db: Session = Depends(database.get_db)
) -> schemas.Game:
    db_game = crud.games.get_game_by_id(db, game_id)
    if db_game.host is not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not the host of this game"
        )
    return db_game

@app.post("/games/{game_id}/add_player")
def add_player(
    game_id: int,
    username: str,
    current_user: Annotated[schemas.User, Depends(get_current_user)],
    db: Session = Depends(database.get_db)
) -> schemas.Game:
    game = crud.games.get_game_by_id(db, game_id)
    if game.host is not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not the host of this game"
        )
    crud.games.add_player(db, game, username)
    return game
    
@app.get("/")
def read_root(current_user: Annotated[schemas.User, Depends(get_current_user)]) -> str:
    return f"Hello, {current_user.username}"