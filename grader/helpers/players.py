"""Helpers to create Player instances in tests.
"""

from sqlmodel import Session

from app.logic.auth import hash_password
from app.models import Player


def make_player(
    session: Session,
    *,
    username: str = "alice",
    email: str | None = None,
    password: str = "x",
    elo: int = 1000,
    is_admin: bool = False,
) -> Player:
    """Create and persist a Player. Use in DB-bound tests."""
    player = Player(
        username=username,
        email=email or f"{username}@example.com",
        password_hash=hash_password(password),
        elo=elo,
        is_admin=is_admin,
    )
    session.add(player)
    session.commit()
    session.refresh(player)
    return player


def build_player(
    *,
    pid: int,
    elo: int = 1500,
    username: str | None = None,
) -> Player:
    """Build an in-memory Player (no DB). Use in pure logic tests."""
    name = username or f"p{pid}"
    return Player(
        id=pid,
        username=name,
        email=f"{name}@example.com",
        password_hash="unused",
        elo=elo,
    )


def build_players(count: int, *, elo: int = 1500) -> list[Player]:
    """Build `count` in-memory players with ids 1..count and identical ELO."""
    return [build_player(pid=i, elo=elo) for i in range(1, count + 1)]
