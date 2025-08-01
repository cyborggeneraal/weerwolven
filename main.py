from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from api import user, database
from api.models import *

app = FastAPI()

origins = ["*"]

#app.include_router(games.routes.router)
#app.include_router(votes.router)
app.include_router(user.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def redirect_docs():
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)

@app.on_event("startup")
def on_startup():
    database.create_db_and_tables()