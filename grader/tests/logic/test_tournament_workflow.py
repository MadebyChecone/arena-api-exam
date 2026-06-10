import pytest

from app.logic.tournament import (
    cancel_tournament,
    create_tournament,
    record_result,
    register_player,
    start_tournament,
)
from app.models import TournamentStatus
from grader.helpers.matches import matches_for_tournament, matches_in_round
from grader.helpers.players import make_player
from grader.helpers.tournaments import make_full_pending_tournament


def test_tournament_creation_validates_bracket_size(session):
    for max_players in (1, 2, 3, 5, 6, 7, 9, 12):
        with pytest.raises(ValueError):
            create_tournament(session, name=f"Bad {max_players}", max_players=max_players)

    four = create_tournament(session, name="Four", max_players=4)
    eight = create_tournament(session, name="Eight", max_players=8)

    assert four.max_players == 4
    assert eight.max_players == 8
    assert four.status == TournamentStatus.PENDING


def test_registration_enforces_roster_rules(session):
    tournament = create_tournament(session, name="Cup", max_players=4)
    alice = make_player(session, username="alice")

    with pytest.raises(ValueError):
        register_player(session, tournament_id=999, player_id=alice.id)
    with pytest.raises(ValueError):
        register_player(session, tournament.id, player_id=999)

    register_player(session, tournament.id, alice.id)
    with pytest.raises(ValueError):
        register_player(session, tournament.id, alice.id)

    for username in ("bob", "carol", "dave"):
        register_player(session, tournament.id, make_player(session, username=username).id)
    extra = make_player(session, username="eve")

    with pytest.raises(ValueError):
        register_player(session, tournament.id, extra.id)


def test_registration_enforces_player_availability(session):
    first = create_tournament(session, name="First", max_players=4)
    second = create_tournament(session, name="Second", max_players=4)
    player = make_player(session, username="alice")

    register_player(session, first.id, player.id)
    session.refresh(player)

    assert player.is_available is False
    with pytest.raises(ValueError):
        register_player(session, second.id, player.id)


def test_state_machine_enforces_action_states(session):
    tournament = make_full_pending_tournament(session, size=4, username_prefix="state")
    start_tournament(session, tournament.id)

    with pytest.raises(ValueError):
        register_player(session, tournament.id, make_player(session, username="late").id)
    with pytest.raises(ValueError):
        start_tournament(session, tournament.id)

    match = matches_in_round(matches_for_tournament(session, tournament.id), round_number=1)[0]
    winner_id = match.player_a_id
    cancel_tournament(session, tournament.id)
    with pytest.raises(ValueError):
        record_result(session, match.id, winner_id=winner_id)

    finished = make_full_pending_tournament(
        session,
        size=4,
        name="Finished Cup",
        username_prefix="finished_state",
    )
    start_tournament(session, finished.id)
    for match in matches_in_round(matches_for_tournament(session, finished.id), round_number=1):
        record_result(session, match.id, winner_id=match.player_a_id)
    final = matches_in_round(matches_for_tournament(session, finished.id), round_number=2)[0]
    record_result(session, final.id, winner_id=final.player_a_id)

    with pytest.raises(ValueError):
        start_tournament(session, finished.id)

