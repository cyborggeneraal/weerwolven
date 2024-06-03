from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse

from api import models, votes, games, user
from api.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(games.router)
#app.include_router(votes.router)
app.include_router(user.router)


@app.get("/")
def redirect_docs():
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)