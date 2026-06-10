from app.models import Match, Player

def _is_power_of_two(n: int) -> bool:
    """Return whether n is a power of two."""
    return n > 0 and (n & (n - 1)) == 0

def seed_players(players: list[Player]) -> list[Player]:
    """Order players for the first round."""
    if len(players) < 4 or not _is_power_of_two(len(players)):
        raise ValueError("number of players must be a power of 2 and at least 4")
    sorted_players = sorted(players, key=lambda p: (-p.elo, p.id))

    seeded: list[Player] = []
    left = 0
    right = len(sorted_players) - 1

    while left < right:
        seeded.append(sorted_players[left])
        seeded.append(sorted_players[right])
        left += 1
        right -= 1


    return seeded


def build_bracket(tournament_id: int, seeded_players: list[Player]) -> list[Match]:
    """Build the first visible matches for a tournament."""

    player_count = len(seeded_players)

    if len(seeded_players) < 4 or not _is_power_of_two(len(seeded_players)):
        raise ValueError("number of players must be a power of 2 and at least 4")

    matches: list[Match] = []
    
    match_in_round = player_count // 2
    round_number = 1
    
    while match_in_round >= 1:
        for slot in range(match_in_round):
            is_final = match_in_round == 1
            if round_number == 1:
                player_a_id = seeded_players[slot * 2].id
                player_b_id = seeded_players[slot * 2 + 1].id
            else:
                player_a_id = None
                player_b_id = None

            matches.append(
                Match(
                    tournament_id=tournament_id,
                    round=round_number,
                    slot_in_round=slot,
                    player_a_id=player_a_id,
                    player_b_id=player_b_id,
                    next_slot=None if is_final else ("a" if slot % 2 == 0 else "b"),
                )
            )
        match_in_round //= 2
        round_number += 1
    return matches
