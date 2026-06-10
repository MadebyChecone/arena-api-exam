"""Helpers to query and filter Match instances in tests."""

from sqlmodel import Session, select

from app.models import Match


def matches_for_tournament(session: Session, tournament_id: int) -> list[Match]:
    """Return all matches of a tournament, in insertion order."""
    return list(
        session.exec(select(Match).where(Match.tournament_id == tournament_id))
    )


def matches_in_round(matches: list[Match], round_number: int) -> list[Match]:
    """Filter matches to a given round, sorted top-to-bottom by slot."""
    in_round = [m for m in matches if m.round == round_number]
    in_round.sort(key=lambda m: m.slot_in_round)
    return in_round
