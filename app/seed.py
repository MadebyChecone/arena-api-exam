"""Seed the local database with playable demo data.

Run from the project root:

    python -m app.seed

If you want to start over, delete arena.db and run the command again.
"""

from sqlmodel import Session, select

from app.database import create_db_and_tables, engine
from app.logic.auth import hash_password
from app.logic.tournament import create_tournament, register_player, start_tournament
from app.models import Player, Tournament

PLAYER_PASSWORD = "password123"
ADMIN_PASSWORD = "admin123"

REGULAR_PLAYERS = [
    ("alice", 1600),
    ("bob", 1500),
    ("carol", 1400),
    ("dave", 1300),
    ("erin", 1550),
    ("frank", 1450),
    ("gina", 1350),
    ("hugo", 1250),
    ("iris", 1520),
    ("jules", 1420),
    ("kai", 1320),
    ("lina", 1220),
]


def main() -> None:
    create_db_and_tables()

    with Session(engine) as session:
        existing_player = session.exec(select(Player)).first()
        existing_tournament = session.exec(select(Tournament)).first()

        if existing_player or existing_tournament:
            print("Database already contains data.")
            print("To reset it, delete arena.db and run python -m app.seed again.")
            return

        create_seed_player(
            session,
            username="admin",
            password=ADMIN_PASSWORD,
            is_admin=True,
            elo=1800,
        )

        players_by_username = {
            username: create_seed_player(
                session,
                username=username,
                password=PLAYER_PASSWORD,
                elo=elo,
            )
            for username, elo in REGULAR_PLAYERS
        }

        create_tournament(session, name="Open Cup", max_players=4)

        ready_cup = create_tournament(session, name="Ready Cup", max_players=4)
        for username in ["alice", "bob", "carol", "dave"]:
            register_player(session, ready_cup.id, players_by_username[username].id)

        started_cup = create_tournament(session, name="Started Cup", max_players=8)
        for username in [
            "erin",
            "frank",
            "gina",
            "hugo",
            "iris",
            "jules",
            "kai",
            "lina",
        ]:
            register_player(session, started_cup.id, players_by_username[username].id)
        start_tournament(session, started_cup.id)

    print("Seed complete.")
    print("\nLogin accounts:")
    print(f"  admin / {ADMIN_PASSWORD}")
    print(f"  regular players / {PLAYER_PASSWORD}")
    print("\nCreated tournaments:")
    print("  Open Cup    - pending, empty, ready for registrations")
    print("  Ready Cup   - pending, full, ready to start")
    print("  Started Cup - in progress, 8 players, ready for match results")


def create_seed_player(
    session: Session,
    username: str,
    password: str,
    *,
    elo: int = 1000,
    is_admin: bool = False,
) -> Player:
    """Create one seeded player with a hashed password."""
    player = Player(
        username=username,
        email=f"{username}@example.com",
        password_hash=hash_password(password),
        elo=elo,
        is_admin=is_admin,
    )
    session.add(player)
    session.commit()
    session.refresh(player)
    return player


if __name__ == "__main__":
    main()
