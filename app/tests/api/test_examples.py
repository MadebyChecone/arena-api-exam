"""Ungraded API test examples.

These tests show how to use the shared pytest fixtures. They are not the exam
contract. The protected tests in `grader/tests/` and the criteria printed by
`make criteria` define the graded behavior.
"""


def test_health_endpoint_returns_ok(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_authenticated_user_can_read_their_profile(auth_client, regular_user):
    response = auth_client.get(f"/api/players/{regular_user.id}")

    assert response.status_code == 200
    assert response.json()["username"] == regular_user.username
