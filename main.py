from typing import Dict, List, Annotated

from jose import jwt, JWTError
from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api import crud, models, schemas, database, votes, games, user
from api.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(games.router)
#app.include_router(votes.router)
app.include_router(user.router)


@app.get("/")
def read_root(current_user: Annotated[schemas.User, Depends(user.auth.get_current_user)]) -> str:
    return f"Hello, {current_user.username}"