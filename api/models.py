from __future__ import annotations
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

class UserBase(SQLModel):
    username: str = Field(index=True)

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    
    #games: List[Game] = Relationship(back_populates="host")
    #players: List[Player] = Relationship(back_populates="user")

class UserCreate(UserBase):
    password: str

class Game(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str | None
    current_day: int = Field(default=0)
    
    host_id: int | None = Field(default=None, foreign_key="user.id")
    #host: User = Relationship(back_populates="games")

    #players: List[Player] = Relationship(back_populates="game")
    #votes: Mapped[Vote] = relationship(back_populates="game")
    
class Player(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    role: str = Field(default="gewone burger")
    team: str = Field(default="burger team")
    health_status: str = Field(default="alive")
    
    game_id: int = Field(foreign_key="game.id")
    #game: Game = Relationship(back_populates="players")

    user_id: int | None = Field(foreign_key="user.id")
    #user: User = Relationship(back_populates="players")
    
#class Vote(SQLModel):
#    __tablename__ = "vote"
#    
#    id: Mapped[int] = mapped_column(primary_key=True, index=True)
#    vote_from: Mapped[str] = mapped_column()
#    game_id: Mapped[int] = mapped_column(ForeignKey("game.id"))
#    day: Mapped[int] = mapped_column()
#    vote_type: Mapped[int] = mapped_column()
    # 0 for lynch
    # 1 for mayor
#    vote_to: Mapped[str] = mapped_column()
    
#    game: Mapped[Game] = relationship(back_populates="votes")

class Action(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    day: int

    player_id: int = Field(foreign_key="player.id")
    #player: Player = Relationship(back_populates="actions")
    #player_targets : List[Player] = relationship(secondary="player_targets_table")


#player_targets_table = Table(
#    "player_targets_table",
#    Base.metadata,
#    Column("action_id", ForeignKey("action.id")),
#    Column("target_id", ForeignKey("player.id"))
#)

#player_targets_info_table = Table(
#    "player_targets_info_table",
#    Base.metadata,
#    Column("info_id", ForeignKey("info.id")),
#    Column("target_id", ForeignKey("player.id"))
#)

#team_targets_info_table = Table(
#    "team_targets_info_table",
#    Base.metadata,
#    Column("info_id", ForeignKey("info.id")),
#    Column("team", String)
#)

class Info(SQLModel, table=True):
    id: int | None = Field(primary_key=True, index=True)
    player_id: int = Field(foreign_key="player.id")
    #player: Player = Relationship(back_populates="infos")
    action_id: int = Field(foreign_key="action.id")
    #action: Action = Relationship(back_populates="infos")
    #player_targets: List[Player] = relationship(secondary=player_targets_info_table)
    #team_targets: List[str] | None = mapped_column(JSON)
    #success : bool | None = mapped_column()