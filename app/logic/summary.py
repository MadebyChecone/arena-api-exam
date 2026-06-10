"""Tournament summary: composite view of state and bracket progress."""

from pydantic import BaseModel
from sqlmodel import Session, select

from app.models import TournamentStatus, Tournament, Match, TournamentPlayer, Player



class ActivePlayer(BaseModel):
    id: int
    username: str


class TournamentSummary(BaseModel):
    tournament_id: int
    name: str
    status: TournamentStatus
    current_round: int
    matches_played: int
    matches_remaining: int
    active_players: list[ActivePlayer]
    is_complete: bool


def tournament_summary(session: Session, tournament_id: int) -> TournamentSummary:
    """Build a summary view of a tournament."""
    tournament = session.get(Tournament, tournament_id)
    if tournament is None:
        raise ValueError(f"tournament {tournament_id} not found")
    
    matches = list(
        session.exec(
            select(Match).where(Match.tournament_id == tournament_id)
        )
    )

    matches_played = sum(1 for match in matches if match.winner_id is not None)
    matches_remaining = sum(1 for match in matches if match.winner_id is None)

    if tournament.status == TournamentStatus.PENDING:
        players = list(
            session.exec(
                select(Player)
                .join(TournamentPlayer, TournamentPlayer.player_id == Player.id)
                .where(TournamentPlayer.tournament_id == tournament_id)
            )
        )
        active_players = [ActivePlayer(id=player.id, username=player.username) for player in players]
        matches_remaining = 0
        current_round = 0

    elif tournament.status == TournamentStatus.FINISHED:
        matches_remaining = 0
        current_round = max((match.round for match in matches), default=0)

        final_match = next(
            (
                match 
                for match in matches 
                if match.round == current_round 
            ),
            None,
        )

        if final_match is not None:
            winner = session.get(Player, final_match.winner_id)
            active_players = (
                [ActivePlayer(id=winner.id, username=winner.username)]
                if winner is not None
                else []
            )

        else:
            active_players = []
        

    else:
        active_player_ids = set()

        for match in matches:
            if match.winner_id is None:
                if match.player_a_id is not None:
                    active_player_ids.add(match.player_a_id)
                if match.player_b_id is not None:
                    active_player_ids.add(match.player_b_id)

        
        if active_player_ids:
            active_players = list(
                session.exec(
                    select(Player).where(Player.id.in_(active_player_ids))
                )
            )  
            active_players = [ActivePlayer(id=player.id, username=player.username) for player in active_players]
        
        else :
            active_players = []

        current_round = min(
            (match.round for match in matches if match.winner_id is None),
            default=0,
        )
    return TournamentSummary(
        tournament_id=tournament.id,
        name=tournament.name,
        status=tournament.status,
        current_round=current_round,
        matches_played=matches_played,
        matches_remaining=matches_remaining,
        active_players=active_players,
        is_complete=tournament.status == TournamentStatus.FINISHED,
    )
