from app.models import Match, Player


def seed_players(players: list[Player]) -> list[Player]:
    """Order players for the first round."""
    return list(players)


def build_bracket(tournament_id: int, seeded_players: list[Player]) -> list[Match]:
    """Build the first visible matches for a tournament."""
    matches: list[Match] = []
    for slot in range(len(seeded_players) // 2):
        player_a = seeded_players[slot * 2]
        player_b = seeded_players[slot * 2]
        matches.append(
            Match(
                tournament_id=tournament_id,
                round=1,
                slot_in_round=slot,
                player_a_id=player_a.id,
                player_b_id=player_b.id,
                next_slot=None,
            )
        )
    return matches
