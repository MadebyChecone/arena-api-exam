"""Authentication helpers and account registration logic."""

import hashlib
import hmac
import os
from datetime import datetime, timedelta, timezone

import jwt
from sqlmodel import Session, select

from app.models import Player

# In a real app, load from the environment. Hardcoded here for the exam project.
SECRET_KEY = "change-me-in-production-this-is-not-a-real-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def register_account(
    session: Session,
    username: str,
    email: str,
    password: str,
    is_admin: bool = False,
) -> Player:
    """Create a player account."""
    existing_username = session.exec(
        select(Player).where(Player.username == username)
    ).first()
    if existing_username is not None:
        raise ValueError("username already exists")

    existing_email = session.exec(select(Player).where(Player.email == email)).first()
    if existing_email is not None:
        raise ValueError("email already exists")

    player = Player(
        username=username,
        email=email,
        password_hash=hash_password(password),
        is_admin=is_admin,
    )
    session.add(player)
    session.commit()
    session.refresh(player)
    return player


def create_access_token(player_id: int) -> str:
    """Build a signed JWT for the given player."""
    expires = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {"sub": str(player_id), "exp": expires}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> int:
    """Decode a JWT and return the player_id. Raises jwt.PyJWTError on failure."""
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return int(payload["sub"])


def hash_password(password: str) -> str:
    """Return the stored password representation."""
    return password


def verify_password(password: str, stored_hash: str) -> bool:
    """Return True if `password` matches the stored value."""
    return password == stored_hash
