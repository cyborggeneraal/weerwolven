from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from api import database
from api import votes
from api.votes import schemas as votes_schemas
from api.votes import crud as votes_crud

router = APIRouter(
    prefix="/voting"
)

@router.get("/{game_id}", response_model=List[votes_schemas.Vote])
def view_votes(game_id: int, db: Session = database.SessionDep):
    return votes_crud.get_votes_from_game_id(db, game_id)

@router.post("/{game_id}", response_model=votes_schemas.Vote)
def post_votes(game_id: int, vote: votes_schemas.VoteCreate, db: Session = database.SessionDep):
    return votes_crud.add_vote(db, game_id, vote)