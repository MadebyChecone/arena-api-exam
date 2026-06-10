from sqlmodel import select

from app.logic.auth import create_access_token, verify_password
from app.models import Player
from grader.helpers.players import make_player
from grader.helpers.tournaments import make_tournament


def test_auth_passwords_are_hashed(client, session):
    response = client.post(
        "/api/auth/register",
        json={"username": "alice", "email": "alice@example.com", "password": "secret"},
    )

    assert response.status_code == 201
    stored = session.exec(select(Player).where(Player.username == "alice")).one()
    assert stored.password_hash != "secret"
    assert verify_password("secret", stored.password_hash)


def test_auth_register_cannot_create_admin(client, session):
    response = client.post(
        "/api/auth/register",
        json={
            "username": "mallory",
            "email": "mallory@example.com",
            "password": "secret",
            "is_admin": True,
        },
    )

    assert response.status_code == 201
    assert response.json()["is_admin"] is False
    stored = session.exec(select(Player).where(Player.username == "mallory")).one()
    assert stored.is_admin is False


def test_auth_responses_do_not_leak_passwords(client, admin_client, session):
    registered = client.post(
        "/api/auth/register",
        json={"username": "alice", "email": "alice@example.com", "password": "secret"},
    )
    assert registered.status_code == 201

    list_response = admin_client.get("/api/players")
    profile_response = admin_client.get(f"/api/players/{registered.json()['id']}")

    for body in (registered.json(), profile_response.json(), *list_response.json()):
        assert "password_hash" not in body
        assert "password" not in body


def test_auth_protected_reads_require_token(client, session):
    tournament = make_tournament(session, name="Private Cup", max_players=4)

    assert client.get("/api/players").status_code == 401
    assert client.get("/api/tournaments").status_code == 401
    assert client.get(f"/api/tournaments/{tournament.id}").status_code == 401


def test_auth_admin_required_for_tournament_creation(client, session):
    regular = make_player(session, username="regular", is_admin=False)
    admin = make_player(session, username="admin", is_admin=True)

    client.headers["Authorization"] = f"Bearer {create_access_token(regular.id)}"
    forbidden = client.post("/api/tournaments", json={"name": "Cup", "max_players": 4})

    client.headers["Authorization"] = f"Bearer {create_access_token(admin.id)}"
    allowed = client.post("/api/tournaments", json={"name": "Admin Cup", "max_players": 4})

    assert forbidden.status_code == 403
    assert allowed.status_code == 201
