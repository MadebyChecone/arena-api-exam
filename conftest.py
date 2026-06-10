# Pytest loads this file automatically.
# The fixtures below replace the real SQLite database with a temporary test database.

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.database import get_session
from app.logic.auth import create_access_token
from app.main import app
from grader.helpers.players import make_player


@pytest.fixture()
def test_engine(tmp_path):
    database_url = f"sqlite:///{tmp_path / 'test.db'}"
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},
    )
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture()
def session(test_engine):
    with Session(test_engine) as session:
        yield session


@pytest.fixture()
def client(test_engine):
    def override_get_session():
        with Session(test_engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def regular_user(session):
    return make_player(session, username="regular", is_admin=False)


@pytest.fixture()
def admin_user(session):
    return make_player(session, username="admin", is_admin=True)


@pytest.fixture()
def auth_client(client, regular_user):
    """A TestClient with a Bearer token for a regular (non-admin) user."""
    client.headers["Authorization"] = f"Bearer {create_access_token(regular_user.id)}"
    return client


@pytest.fixture()
def admin_client(client, admin_user):
    """A TestClient with a Bearer token for an admin user."""
    client.headers["Authorization"] = f"Bearer {create_access_token(admin_user.id)}"
    return client
