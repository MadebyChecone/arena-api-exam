"""Tournament summary: composite view of state and bracket progress."""

from pydantic import BaseModel
from sqlmodel import Session

from app.models import TournamentStatus


class ActivePlayer(BaseModel):
    id: int
    username: str


class TournamentSummary(BaseModel):
    tournament_id: int
    name: str
    status: TournamentStatus
    current_round: int
    matches_played: int
    matches_remaining: int
    active_players: list[ActivePlayer]
    is_complete: bool


def tournament_summary(session: Session, tournament_id: int) -> TournamentSummary:
    """Build a summary view of a tournament."""
    return TournamentSummary(
        tournament_id=tournament_id,
        name="",
        status=TournamentStatus.PENDING,
        current_round=0,
        matches_played=0,
        matches_remaining=0,
        active_players=[],
        is_complete=False,
    )
