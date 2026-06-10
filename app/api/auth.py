"""Authentication endpoints and FastAPI dependencies."""

from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlmodel import select

from app.database import SessionDep
from app.logic.auth import (
    create_access_token,
    decode_access_token,
    register_account,
    verify_password,
)
from app.models import Player

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


class RegisterAccountRequest(BaseModel):
    username: str
    email: str
    password: str
    is_admin: bool = False


class RegisteredPlayer(BaseModel):
    id: int
    username: str
    email: str
    elo: int
    is_admin: bool


@router.post("/register", status_code=201, response_model=RegisteredPlayer)
def register(
    body: RegisterAccountRequest,
    session: SessionDep,
) -> Player:
    """Create a regular player account."""
    try:
        return register_account(
            session,
            username=body.username,
            email=body.email,
            password=body.password,
            is_admin=body.is_admin,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
) -> dict[str, str]:
    """Exchange username + password for a bearer token."""
    player = session.exec(
        select(Player).where(Player.username == form.username)
    ).first()
    if player is None or not verify_password(form.password, player.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": create_access_token(player.id), "token_type": "bearer"}


def require_admin(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep,
) -> Player:
    """Allow only admin users; 403 otherwise."""
    current_user = get_current_user(token, session)
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")
    return current_user


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep,
) -> Player:
    """Resolve the bearer token to the calling Player. 401 on failure."""
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        player_id = decode_access_token(token)
    except jwt.PyJWTError:
        raise unauthorized
    player = session.get(Player, player_id)
    if player is None:
        raise unauthorized
    return player


# Typing aliases for endpoint signatures.
CurrentUser = Annotated[Player, Depends(get_current_user)]
AdminUser = Annotated[Player, Depends(require_admin)]
