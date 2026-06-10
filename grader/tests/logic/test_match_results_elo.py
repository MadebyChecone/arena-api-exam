import pytest

from app.logic.auth import create_access_token
from app.logic.elo import compute_new_ratings, expected_score
from app.logic.tournament import record_result, start_tournament
from app.models import Player, Tournament, TournamentStatus
from grader.helpers.matches import matches_for_tournament, matches_in_round
from grader.helpers.players import make_player
from grader.helpers.tournaments import make_full_pending_tournament


def test_elo_formula_is_correct():
    assert expected_score(1500, 1500) == 0.5
    assert expected_score(1700, 1500) > 0.5
    assert expected_score(1500, 1700) < 0.5

    winner, loser = compute_new_ratings(1500, 1500, score_a=1.0, k=32)
    assert (winner, loser) == (1516, 1484)

    underdog, _ = compute_new_ratings(1400, 1600, score_a=1.0, k=32)
    favorite, _ = compute_new_ratings(1600, 1400, score_a=1.0, k=32)
    assert (underdog - 1400) > (favorite - 1600)
    assert all(isinstance(rating, int) for rating in compute_new_ratings(1234, 1567, score_a=0.5))


def test_match_result_permissions(client, session):
    outsider = make_player(session, username="outsider")
    admin = make_player(session, username="admin", is_admin=True)

    first = make_full_pending_tournament(session, size=4, username_prefix="perm_first")
    start_tournament(session, first.id)
    first_match = matches_in_round(matches_for_tournament(session, first.id), round_number=1)[0]

    client.headers["Authorization"] = f"Bearer {create_access_token(outsider.id)}"
    forbidden = client.post(
        f"/api/matches/{first_match.id}/result",
        json={"winner_id": first_match.player_a_id},
    )

    client.headers["Authorization"] = f"Bearer {create_access_token(first_match.player_a_id)}"
    participant = client.post(
        f"/api/matches/{first_match.id}/result",
        json={"winner_id": first_match.player_a_id},
    )

    second = make_full_pending_tournament(
        session,
        size=4,
        name="Admin Result Cup",
        username_prefix="perm_second",
    )
    start_tournament(session, second.id)
    second_match = matches_in_round(matches_for_tournament(session, second.id), round_number=1)[0]

    client.headers["Authorization"] = f"Bearer {create_access_token(admin.id)}"
    admin_response = client.post(
        f"/api/matches/{second_match.id}/result",
        json={"winner_id": second_match.player_a_id},
    )

    assert forbidden.status_code == 403
    assert participant.status_code == 200
    assert admin_response.status_code == 200


def test_match_result_validates_inputs(session):
    tournament = make_full_pending_tournament(session, size=4, username_prefix="validate_result")
    start_tournament(session, tournament.id)
    round_1 = matches_in_round(matches_for_tournament(session, tournament.id), round_number=1)
    first_match = round_1[0]
    final = matches_in_round(matches_for_tournament(session, tournament.id), round_number=2)[0]
    outsider = make_player(session, username="outsider")

    with pytest.raises(ValueError):
        record_result(session, match_id=999, winner_id=1)
    with pytest.raises(ValueError):
        record_result(session, final.id, winner_id=1)
    with pytest.raises(ValueError):
        record_result(session, first_match.id, winner_id=outsider.id)

    record_result(session, first_match.id, winner_id=first_match.player_a_id)
    with pytest.raises(ValueError):
        record_result(session, first_match.id, winner_id=first_match.player_b_id)


def test_match_result_advances_and_finishes(session):
    tournament = make_full_pending_tournament(session, size=4, username_prefix="advance_result")
    start_tournament(session, tournament.id)
    top, bottom = matches_in_round(matches_for_tournament(session, tournament.id), round_number=1)

    record_result(session, top.id, winner_id=top.player_a_id)
    record_result(session, bottom.id, winner_id=bottom.player_b_id)

    final = matches_in_round(matches_for_tournament(session, tournament.id), round_number=2)[0]
    assert final.player_a_id == top.player_a_id
    assert final.player_b_id == bottom.player_b_id

    record_result(session, final.id, winner_id=final.player_a_id)
    refreshed = session.get(Tournament, tournament.id)
    assert refreshed.status == TournamentStatus.FINISHED


def test_match_result_updates_elo(session):
    tournament = make_full_pending_tournament(session, size=4, username_prefix="elo_result")
    start_tournament(session, tournament.id)
    match = matches_in_round(matches_for_tournament(session, tournament.id), round_number=1)[0]
    winner_before = session.get(Player, match.player_a_id).elo
    loser_before = session.get(Player, match.player_b_id).elo

    record_result(session, match.id, winner_id=match.player_a_id)

    winner_after = session.get(Player, match.player_a_id).elo
    loser_after = session.get(Player, match.player_b_id).elo
    assert winner_after > winner_before
    assert loser_after < loser_before
