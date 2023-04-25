from fastapi import APIRouter

from api import crud

voting_router = APIRouter(
    prefix="/voting"
)

@voting_router.get("/{game_id}")
def view_votes(game_id: int):
    pass