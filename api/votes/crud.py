from typing import List, Any

from sqlalchemy.orm import Session

from api import schemas, models, games
from api.votes import schemas as votes_schemas

def get_votes_from_game_id(db: Session, game_id: int) -> List[Any]:
    return db.query(models.Vote).filter(models.Vote.game_id == game_id).all()

def add_vote(db: Session, game_id: int, vote: votes_schemas.VoteCreate) -> models.Vote:
    db_game = games.crud.get_game_by_id(db, game_id)
    db_vote = models.Vote(
        vote_from = vote.vote_from,
        vote_to = vote.vote_to,
        game_id = game_id,
        day = db_game.current_day,
        vote_type = vote.vote_type.value
    )
    db.add(db_vote)
    db.commit()
    db.refresh(db_vote)
    return db_vote