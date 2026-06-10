"""Ungraded logic/database test examples.

These tests show how to use the `session` fixture and test helpers. They are not
the exam contract. The protected tests in `grader/tests/` and the criteria
printed by `make criteria` define the graded behavior.
"""

from app.models import Player
from grader.helpers.players import make_player


def test_can_create_player_in_test_database(session):
    player = make_player(session, username="alice")

    stored = session.get(Player, player.id)

    assert stored is not None
    assert stored.username == "alice"
