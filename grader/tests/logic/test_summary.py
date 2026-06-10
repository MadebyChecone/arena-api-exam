import pytest

from app.logic.summary import tournament_summary
from app.logic.tournament import record_result, start_tournament
from app.models import TournamentStatus
from grader.helpers.matches import matches_for_tournament, matches_in_round
from grader.helpers.tournaments import make_full_pending_tournament


def test_summary_logic_pending_and_unknown(session):
    tournament = make_full_pending_tournament(
        session,
        size=4,
        name="Summary Cup",
        username_prefix="summary_pending",
    )

    summary = tournament_summary(session, tournament.id)

    assert summary.tournament_id == tournament.id
    assert summary.name == "Summary Cup"
    assert summary.status == TournamentStatus.PENDING
    assert summary.current_round == 0
    assert summary.matches_played == 0
    assert summary.matches_remaining == 0
    assert len(summary.active_players) == 4
    assert summary.is_complete is False

    with pytest.raises(ValueError):
        tournament_summary(session, tournament_id=999)


def test_summary_logic_progress_and_active_players(session):
    tournament = make_full_pending_tournament(
        session,
        size=4,
        username_prefix="summary_progress",
    )
    start_tournament(session, tournament.id)

    started = tournament_summary(session, tournament.id)
    assert started.status == TournamentStatus.IN_PROGRESS
    assert started.current_round == 1
    assert started.matches_played == 0
    assert started.matches_remaining == 3
    assert len(started.active_players) == 4

    for match in matches_in_round(matches_for_tournament(session, tournament.id), round_number=1):
        record_result(session, match.id, winner_id=match.player_a_id)

    after_round_1 = tournament_summary(session, tournament.id)
    assert after_round_1.current_round == 2
    assert after_round_1.matches_played == 2
    assert after_round_1.matches_remaining == 1
    assert len(after_round_1.active_players) == 2
