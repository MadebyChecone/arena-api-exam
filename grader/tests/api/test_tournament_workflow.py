from sqlmodel import select

from app.logic.auth import create_access_token
from app.logic.tournament import record_result, start_tournament
from app.models import Player, TournamentStatus
from grader.helpers.matches import matches_for_tournament, matches_in_round
from grader.helpers.players import make_player
from grader.helpers.tournaments import make_full_pending_tournament, make_tournament


def test_registration_permissions_self_or_admin(client, session):
    regular = make_player(session, username="regular", is_admin=False)
    admin = make_player(session, username="admin", is_admin=True)
    other = make_player(session, username="other")

    self_tournament = make_tournament(session, name="Self Cup", max_players=4)
    client.headers["Authorization"] = f"Bearer {create_access_token(regular.id)}"
    self_response = client.post(
        f"/api/tournaments/{self_tournament.id}/players",
        json={"player_id": regular.id},
    )

    other_tournament = make_tournament(session, name="Other Cup", max_players=4)
    forbidden = client.post(
        f"/api/tournaments/{other_tournament.id}/players",
        json={"player_id": other.id},
    )

    admin_tournament = make_tournament(session, name="Admin Cup", max_players=4)
    client.headers["Authorization"] = f"Bearer {create_access_token(admin.id)}"
    admin_response = client.post(
        f"/api/tournaments/{admin_tournament.id}/players",
        json={"player_id": other.id},
    )

    assert self_response.status_code == 201
    assert forbidden.status_code == 403
    assert admin_response.status_code == 201


def test_cancellation_transitions_and_frees_players(client, session):
    regular = make_player(session, username="regular", is_admin=False)
    admin = make_player(session, username="admin", is_admin=True)

    pending = make_full_pending_tournament(
        session,
        size=4,
        name="Pending Cup",
        username_prefix="pending_cancel",
    )
    client.headers["Authorization"] = f"Bearer {create_access_token(regular.id)}"
    forbidden = client.post(f"/api/tournaments/{pending.id}/cancel")

    client.headers["Authorization"] = f"Bearer {create_access_token(admin.id)}"
    cancelled = client.post(f"/api/tournaments/{pending.id}/cancel")

    assert forbidden.status_code == 403
    assert cancelled.status_code == 200
    assert cancelled.json()["status"] == TournamentStatus.CANCELLED.value
    registered_players = session.exec(select(Player).where(Player.username.startswith("pending_cancel_"))).all()
    assert all(p.is_available for p in registered_players)

    in_progress = make_full_pending_tournament(
        session,
        size=4,
        name="Running Cup",
        username_prefix="running_cancel",
    )
    start_tournament(session, in_progress.id)
    cancelled_running = client.post(f"/api/tournaments/{in_progress.id}/cancel")
    assert cancelled_running.status_code == 200
    assert cancelled_running.json()["status"] == TournamentStatus.CANCELLED.value

    finished = make_full_pending_tournament(
        session,
        size=4,
        name="Finished Cup",
        username_prefix="finished_cancel",
    )
    start_tournament(session, finished.id)
    for match in matches_in_round(matches_for_tournament(session, finished.id), round_number=1):
        record_result(session, match.id, winner_id=match.player_a_id)
    final = matches_in_round(matches_for_tournament(session, finished.id), round_number=2)[0]
    record_result(session, final.id, winner_id=final.player_a_id)

    rejected = client.post(f"/api/tournaments/{finished.id}/cancel")
    assert rejected.status_code == 400
