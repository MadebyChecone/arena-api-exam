from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlmodel import select

from app.api.auth import CurrentUser
from app.api.auth import AdminUser
from app.database import SessionDep
from app.logic.summary import TournamentSummary, tournament_summary
from app.logic.tournament import (
    cancel_tournament,
    create_tournament,
    register_player,
    start_tournament,
)
from app.models import Match, Tournament

router = APIRouter(prefix="/tournaments", tags=["tournaments"])


class CreateTournamentRequest(BaseModel):
    name: str
    max_players: int


class RegisterPlayerRequest(BaseModel):
    player_id: int


@router.post("", status_code=201, response_model=Tournament)
def create_tournament_endpoint(
    body: CreateTournamentRequest,
    session: SessionDep,
    admin_user: AdminUser,
) -> Tournament:
    try:
        return create_tournament(session, name=body.name, max_players=body.max_players)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[Tournament])
def list_tournaments(session: SessionDep, current_user: CurrentUser) -> list[Tournament]:
    return list(session.exec(select(Tournament).order_by(Tournament.name)).all())


@router.get("/{tournament_id}")
def get_tournament(
    tournament_id: int,
    session: SessionDep,
    current_user: CurrentUser,
) -> dict:
    tournament = session.get(Tournament, tournament_id)
    if tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found")
    matches = list(
        session.exec(select(Match).where(Match.tournament_id == tournament_id))
    )
    return {"tournament": tournament, "matches": matches}


@router.post("/{tournament_id}/players", status_code=201)
def register_player_endpoint(
    tournament_id: int,
    body: RegisterPlayerRequest,
    session: SessionDep,
    current_user: CurrentUser,
) -> dict[str, int]:
    if not current_user.is_admin and current_user.id != body.player_id:
        raise HTTPException(status_code=403, detail="Not authorized to register this player")
    try:
        register_player(session, tournament_id, body.player_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"tournament_id": tournament_id, "player_id": body.player_id}


@router.post("/{tournament_id}/start", response_model=Tournament)
def start_tournament_endpoint(
    tournament_id: int,
    session: SessionDep,
    current_user: CurrentUser,
) -> Tournament:
    try:
        return start_tournament(session, tournament_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{tournament_id}/cancel", response_model=Tournament)
def cancel_tournament_endpoint(
    tournament_id: int,
    session: SessionDep,
    admin_user: AdminUser,
) -> Tournament:
    try:
        return cancel_tournament(session, tournament_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{tournament_id}/summary", response_model=TournamentSummary)
def get_tournament_summary(
    tournament_id: int,
    session: SessionDep,
    current_user: CurrentUser,
) -> TournamentSummary:
    try:
        return tournament_summary(session, tournament_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
