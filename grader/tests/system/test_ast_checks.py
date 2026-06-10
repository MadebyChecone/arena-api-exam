"""Smoke tests for the AST-based student-test checker.

Proves the checker accepts well-formed tests and rejects trivial cheats.
"""

import textwrap
from pathlib import Path

from grader.criteria import StudentTestCriterion
from grader.engine.ast_checks import check_student_test

CRITERION = StudentTestCriterion(
    id="example",
    points=1,
    file="app/tests/test_x.py",
    function="test_listing",
    prompt="Write a test that calls the endpoint and checks the response.",
    expected_calls=("client.get('/api/players')",),
    expected_asserts=(
        "response.status_code == 200",
        "response.json() == []",
    ),
)


def _write(project_root: Path, source: str) -> None:
    test_file = project_root / "app" / "tests" / "test_x.py"
    test_file.parent.mkdir(parents=True, exist_ok=True)
    test_file.write_text(textwrap.dedent(source).lstrip())


def test_accepts_well_formed_student_test(tmp_path):
    _write(tmp_path, """
        def test_listing(client):
            response = client.get('/api/players')
            assert response.status_code == 200
            assert response.json() == []
    """)

    ok, problems = check_student_test(CRITERION, project_root=tmp_path)

    assert ok, problems


def test_normalises_quote_style(tmp_path):
    _write(tmp_path, """
        def test_listing(client):
            response = client.get("/api/players")
            assert response.status_code == 200
            assert response.json() == []
    """)

    ok, _ = check_student_test(CRITERION, project_root=tmp_path)

    assert ok


def test_rejects_trivial_test(tmp_path):
    _write(tmp_path, """
        def test_listing(client):
            assert True
    """)

    ok, problems = check_student_test(CRITERION, project_root=tmp_path)

    assert not ok
    assert any("client.get('/api/players')" in p for p in problems)
    assert any("response.status_code == 200" in p for p in problems)
    assert any("Write a test" in p for p in problems)
    assert any("Add an assertion equivalent" in p for p in problems)


def test_rejects_asserts_that_dont_check_the_response(tmp_path):
    _write(tmp_path, """
        def test_listing(client):
            response = client.get('/api/players')
            assert 200 == 200
            assert [] == []
    """)

    ok, problems = check_student_test(CRITERION, project_root=tmp_path)

    assert not ok
    assert any("response.status_code == 200" in p for p in problems)
    assert any("response.json() == []" in p for p in problems)


def test_rejects_missing_function(tmp_path):
    _write(tmp_path, """
        def test_other_name(client):
            pass
    """)

    ok, problems = check_student_test(CRITERION, project_root=tmp_path)

    assert not ok
    assert any("Missing test function: test_listing" in p for p in problems)


def test_rejects_missing_file(tmp_path):
    ok, problems = check_student_test(CRITERION, project_root=tmp_path)

    assert not ok
    assert any("Missing test file" in p for p in problems)
