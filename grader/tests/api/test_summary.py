from app.logic.tournament import record_result, start_tournament
from app.models import TournamentStatus
from grader.helpers.matches import matches_for_tournament, matches_in_round
from grader.helpers.tournaments import make_full_pending_tournament


def test_summary_endpoint_finished_response(admin_client, session):
    missing = admin_client.get("/api/tournaments/999/summary")
    assert missing.status_code == 404

    tournament = make_full_pending_tournament(
        session,
        size=4,
        name="Finished Summary Cup",
        username_prefix="summary_finished",
    )
    start_tournament(session, tournament.id)
    for match in matches_in_round(matches_for_tournament(session, tournament.id), round_number=1):
        record_result(session, match.id, winner_id=match.player_a_id)
    final = matches_in_round(matches_for_tournament(session, tournament.id), round_number=2)[0]
    record_result(session, final.id, winner_id=final.player_a_id)

    response = admin_client.get(f"/api/tournaments/{tournament.id}/summary")

    assert response.status_code == 200
    body = response.json()
    assert body["tournament_id"] == tournament.id
    assert body["name"] == "Finished Summary Cup"
    assert body["status"] == TournamentStatus.FINISHED.value
    assert body["matches_played"] == 3
    assert body["matches_remaining"] == 0
    assert body["is_complete"] is True
    assert len(body["active_players"]) == 1
