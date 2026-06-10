from datetime import datetime, timezone
from enum import Enum

from sqlmodel import Field, SQLModel


class TournamentStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"
    CANCELLED = "cancelled"


class Player(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    username: str = Field(index=True, unique=True)
    password_hash: str
    elo: int = 1000
    is_available: bool = True
    is_admin: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Tournament(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    status: TournamentStatus = Field(default=TournamentStatus.PENDING, index=True)
    max_players: int


class TournamentPlayer(SQLModel, table=True):
    tournament_id: int = Field(foreign_key="tournament.id", primary_key=True)
    player_id: int = Field(foreign_key="player.id", primary_key=True)


class Match(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tournament_id: int = Field(foreign_key="tournament.id")
    round: int
    slot_in_round: (
        int  # 0-indexed position within the round_number (top-to-bottom display order)
    )
    player_a_id: int | None = Field(default=None, foreign_key="player.id")
    player_b_id: int | None = Field(default=None, foreign_key="player.id")
    winner_id: int | None = Field(default=None, foreign_key="player.id")
    next_slot: str | None = None  # "a" or "b"
