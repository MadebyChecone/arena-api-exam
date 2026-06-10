from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlmodel import select

from app.api.auth import CurrentUser
from app.database import SessionDep
from app.models import Player

router = APIRouter(prefix="/players", tags=["players"])


class PlayerPublic(BaseModel):
    """Player data returned by the API."""

    id: int
    username: str
    email: str
    elo: int
    is_admin: bool


@router.get("", response_model=list[PlayerPublic])
def list_players(session: SessionDep, current_user: CurrentUser) -> list[Player]:
    return list(session.exec(select(Player).order_by(Player.username)).all())


@router.get("/{player_id}", response_model=PlayerPublic)
def get_player(
    player_id: int,
    session: SessionDep,
    current_user: CurrentUser,
) -> Player:
    player = session.get(Player, player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return player
