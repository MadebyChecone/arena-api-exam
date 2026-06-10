"""Helpers to create Tournament instances in tests."""

from sqlmodel import Session

from app.logic.tournament import create_tournament, register_player
from app.models import Tournament, TournamentStatus
from grader.helpers.players import make_player


def make_tournament(
    session: Session,
    *,
    name: str = "Cup",
    max_players: int = 8,
    status: TournamentStatus = TournamentStatus.PENDING,
) -> Tournament:
    """Insert a Tournament directly. Bypasses validation; use for edge-case tests."""
    tournament = Tournament(name=name, max_players=max_players, status=status)
    session.add(tournament)
    session.commit()
    session.refresh(tournament)
    return tournament


def make_full_pending_tournament(
    session: Session,
    *,
    size: int,
    name: str = "Cup",
    username_prefix: str = "player",
) -> Tournament:
    """Create a tournament and register `size` players. Status stays PENDING."""
    tournament = create_tournament(session, name=name, max_players=size)
    for i in range(size):
        player = make_player(session, username=f"{username_prefix}_{i}", elo=1500 + i * 10)
        register_player(session, tournament.id, player.id)
    return tournament
