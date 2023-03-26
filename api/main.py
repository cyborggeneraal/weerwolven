from typing import Dict, List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from api import crud, models, schemas
from api.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.post("/users")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)) -> schemas.User:
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> List[schemas.User]:
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)) -> schemas.User:
    db_user = crud.get_user(db, user_id= user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/")
def read_root() -> Dict[str, str]:
    return {"Hello": "World"}