from sqlmodel import select

from app.logic.auth import register_account
from app.logic.summary import tournament_summary
from app.logic.tournament import (
    create_tournament,
    register_player,
    start_tournament,
    record_result,
)
from app.models import Match, TournamentStatus

def test_summary_for_pending_tournament(session):
    tournament = create_tournament(session, name="Test Tournament", max_players=4)

    players = [
        register_account(
            session,
            username=f"player{i}",
            email=f"player{i}@exmple.com",
            password="password",
        )
        for i in range(4)
    ]

    for player in players:
        register_player(session, tournament_id=tournament.id, player_id=player.id)

    summary = tournament_summary(session, tournament.id)

    assert summary.tournament_id == tournament.id
    assert summary.name == tournament.name
    assert summary.status == TournamentStatus.PENDING
    assert summary.matches_played == 0
    assert summary.matches_remaining == 0
    assert len(summary.active_players) == 4
    assert summary.is_complete is False


def test_summary_after_first_round_results(session):
    tournament = create_tournament(session, name="Test Tournament", max_players=4)


    players = [
        register_account(
            session,
            username=f"progress_player{i}",
            email=f"progress_player{i}@example.com",
            password="password",
        )
        for i in range(4)
    ]

    for player in players:
        register_player(session, tournament_id=tournament.id, player_id=player.id)

    start_tournament(session, tournament.id)


    first_round_matches = list(
        session.exec(
            select(Match)
            .where(Match.tournament_id == tournament.id)
            .where(Match.round == 1)
            .order_by(Match.slot_in_round)
        )
    )

    for match in first_round_matches:
        record_result(session, match.id, winner_id=match.player_a_id)

    summary = tournament_summary(session, tournament.id)

    assert summary.current_round == 2
    assert summary.matches_played == 2
    assert summary.matches_remaining == 1
    assert len(summary.active_players) == 2
    assert summary.is_complete is False
