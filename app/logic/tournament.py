from sqlmodel import Session, select

from app.logic.bracket import build_bracket, seed_players
from app.logic.elo import compute_new_ratings
from app.logic.tournament_state import validate_transition, is_terminal
from app.models import Match, Player, Tournament, TournamentPlayer, TournamentStatus


def create_tournament(session: Session, name: str, max_players: int) -> Tournament:
    """Create a pending tournament."""
    if max_players < 4 or (max_players & (max_players - 1)) != 0:
        raise ValueError("max_players must be a power of 2 and at least 4")
    tournament = Tournament(
        name=name,
        max_players=max_players,
        status=TournamentStatus.PENDING,
    )
    session.add(tournament)
    session.commit()
    session.refresh(tournament)
    return tournament


def register_player(session: Session, tournament_id: int, player_id: int) -> Tournament:
    """Add a player to a tournament."""
    tournament = session.get(Tournament, tournament_id)
    if tournament is None:
        raise ValueError(f"tournament {tournament_id} not found")

    player = session.get(Player, player_id)

    if player is None:
        raise ValueError(f"player {player_id} not found")

    if tournament.status != TournamentStatus.PENDING:
        raise ValueError(f"tournament {tournament_id} is not accepting registrations")
    
    if not player.is_available:
        raise ValueError(f"player {player_id} is not available for registration")

    existing_registration = session.exec(
        select(TournamentPlayer).where(
            TournamentPlayer.tournament_id == tournament_id,
            TournamentPlayer.player_id == player_id,
        )
    ).first()

    if existing_registration is not None:
        raise ValueError(f"player already registered")

    registered_player = session.exec(
        select(TournamentPlayer).where(
            TournamentPlayer.tournament_id == tournament_id
        )
    ).all()   
    
    if len(registered_player) >= tournament.max_players:
        raise ValueError(f"tournament is already full")

    session.add(TournamentPlayer(tournament_id=tournament_id, player_id=player_id))
    player.is_available = False
    session.add(player)

    session.commit()
    session.refresh(tournament)
    return tournament


def start_tournament(session: Session, tournament_id: int) -> Tournament:
    """Seed the registered players, materialize matches, and start the tournament."""
    tournament = session.get(Tournament, tournament_id)
    if tournament is None:
        raise ValueError(f"tournament {tournament_id} not found")
    validate_transition(tournament.status, TournamentStatus.IN_PROGRESS)

    players = _registered_players(session, tournament_id)
    if len(players) != tournament.max_players:
        raise ValueError(
            f"tournament {tournament_id} needs "
            f"{tournament.max_players} players, has {len(players)}"
        )

    seeded = seed_players(players)
    matches = build_bracket(tournament_id=tournament_id, seeded_players=seeded)
    session.add_all(matches)

    tournament.status = TournamentStatus.IN_PROGRESS
    session.add(tournament)
    session.commit()
    session.refresh(tournament)
    return tournament


def record_result(session: Session, match_id: int, winner_id: int) -> Match:
    """Record the winner and advance the tournament."""
    match = session.get(Match, match_id)
    if match is None:
        raise ValueError(f"match {match_id} not found")

    tournament = session.get(Tournament, match.tournament_id)
    if tournament.status != TournamentStatus.IN_PROGRESS:
        raise ValueError(f"tournament {tournament.id} is not in progress")
    
   
    match.winner_id = winner_id
    session.add(match)
    _update_elo(session, match, winner_id)

    if match.next_slot is None:
        validate_transition(tournament.status, TournamentStatus.FINISHED)
        tournament.status = TournamentStatus.FINISHED
        session.add(tournament)

        _free_registered_players(session, tournament.id)
    else:
        parent = session.exec(
            select(Match).where(
                Match.tournament_id == match.tournament_id,
                Match.round == match.round + 1,
                Match.slot_in_round == match.slot_in_round // 2,
            )
        ).one()
        if match.next_slot == "a":
            parent.player_b_id = winner_id
        else:
            parent.player_a_id = winner_id
        session.add(parent)

    session.commit()
    session.refresh(match)
    return match


def cancel_tournament(session: Session, tournament_id: int) -> Tournament:
    """Cancel a tournament."""
    tournament = session.get(Tournament, tournament_id)
    if tournament is None:
        raise ValueError(f"tournament {tournament_id} not found")
    validate_transition(tournament.status, TournamentStatus.CANCELLED)

    tournament.status = TournamentStatus.CANCELLED
    session.add(tournament)

    _free_registered_players(session, tournament_id)

    session.commit()
    session.refresh(tournament)
    return tournament


def _registered_players(session: Session, tournament_id: int) -> list[Player]:
    return list(
        session.exec(
            select(Player)
            .join(TournamentPlayer, TournamentPlayer.player_id == Player.id)
            .where(TournamentPlayer.tournament_id == tournament_id)
        )
    )


def _free_registered_players(session: Session, tournament_id: int) -> None:
    """Set all registered players as available."""
    for player in _registered_players(session, tournament_id):
        player.is_available = True
        session.add(player)


def _update_elo(session: Session, match: Match, winner_id: int) -> None:
    """Apply ELO updates to both players after a match result."""
    loser_id = (
        match.player_a_id if match.player_b_id == winner_id else match.player_b_id
    )
    winner = session.get(Player, winner_id)
    loser = session.get(Player, loser_id)
    if winner is None or loser is None:
        return
    new_winner_elo, new_loser_elo = compute_new_ratings(
        rating_a=winner.elo,
        rating_b=loser.elo,
        score_a=1.0,
    )
    winner.elo = new_winner_elo
    loser.elo = new_loser_elo
    session.add(winner)
    session.add(loser)
