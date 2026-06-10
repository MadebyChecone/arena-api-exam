import pytest

from app.logic.bracket import build_bracket, seed_players
from app.logic.tournament import start_tournament
from app.models import TournamentStatus
from grader.helpers.matches import matches_for_tournament, matches_in_round
from grader.helpers.players import build_player, build_players
from grader.helpers.tournaments import make_full_pending_tournament


def test_bracket_seed_players_by_elo():
    players_4 = [build_player(pid=i, elo=2000 - i * 100) for i in range(1, 5)]
    players_8 = [build_player(pid=i, elo=2000 - i * 50) for i in range(1, 9)]

    seeded_4 = seed_players(players_4)
    seeded_8 = seed_players(players_8)

    assert [p.id for p in seeded_4] == [1, 4, 2, 3]
    assert [p.id for p in seeded_8] == [1, 8, 2, 7, 3, 6, 4, 5]


def test_bracket_seed_tiebreak_is_deterministic():
    players = [
        build_player(pid=4, elo=1500),
        build_player(pid=2, elo=1500),
        build_player(pid=3, elo=1500),
        build_player(pid=1, elo=1500),
    ]

    seeded = seed_players(players)

    assert [p.id for p in seeded] == [1, 4, 2, 3]


def test_bracket_validates_player_count():
    for count in (1, 2, 3, 5, 6, 7, 9, 12):
        with pytest.raises(ValueError):
            build_bracket(tournament_id=1, seeded_players=build_players(count))

    assert len(build_bracket(tournament_id=1, seeded_players=build_players(4))) == 3


def test_bracket_materializes_match_tree():
    matches_4 = build_bracket(tournament_id=1, seeded_players=build_players(4))
    matches_8 = build_bracket(tournament_id=1, seeded_players=build_players(8))

    assert len(matches_4) == 3
    assert len(matches_in_round(matches_4, round_number=1)) == 2
    assert len(matches_in_round(matches_4, round_number=2)) == 1

    assert len(matches_8) == 7
    assert len(matches_in_round(matches_8, round_number=1)) == 4
    assert len(matches_in_round(matches_8, round_number=2)) == 2
    assert len(matches_in_round(matches_8, round_number=3)) == 1

    for match in matches_in_round(matches_4, round_number=1):
        assert match.player_a_id is not None
        assert match.player_b_id is not None
    final = matches_in_round(matches_4, round_number=2)[0]
    assert final.player_a_id is None
    assert final.player_b_id is None


def test_bracket_wires_advancement_slots(session):
    matches = build_bracket(tournament_id=1, seeded_players=build_players(8))

    round_1 = matches_in_round(matches, round_number=1)
    round_2 = matches_in_round(matches, round_number=2)
    final = matches_in_round(matches, round_number=3)[0]

    assert [(m.player_a_id, m.player_b_id) for m in round_1] == [
        (1, 2),
        (3, 4),
        (5, 6),
        (7, 8),
    ]
    assert [m.next_slot for m in round_1] == ["a", "b", "a", "b"]
    assert [m.next_slot for m in round_2] == ["a", "b"]
    assert final.next_slot is None

    tournament = make_full_pending_tournament(
        session,
        size=4,
        username_prefix="bracket_start",
    )
    started = start_tournament(session, tournament.id)

    assert started.status == TournamentStatus.IN_PROGRESS
    assert len(matches_for_tournament(session, tournament.id)) == 3
