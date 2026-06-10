"""Criterion data classes, an implementation detail of the criteria package.

Two kinds:
- BehaviorCriterion:    instructor test under grader/tests/.
                        Pass = the test passes. No AST checks needed
                        because the file is protected by reviewed_files.py.
- StudentTestCriterion: a test the student must write under app/tests/.
                        Pass = AST checks pass AND the test passes.

`category` is injected by criteria/__init__.py from the module name.
Do not set it by hand.
"""

from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class Criterion:
    id: str
    points: int
    file: str       # e.g. "grader/tests/api/test_players.py"
    function: str   # e.g. "test_listing_returns_empty_array"
    category: str = ""

    @property
    def nodeid(self) -> str:
        return f"{self.file}::{self.function}"


@dataclass(frozen=True, kw_only=True)
class BehaviorCriterion(Criterion):
    description: str


@dataclass(frozen=True, kw_only=True)
class StudentTestCriterion(Criterion):
    prompt: str = ""                         # human-readable task shown by make criteria
    expected_calls: tuple[str, ...] = ()    # e.g. ("client.get('/api/players')",)
    expected_asserts: tuple[str, ...] = ()  # e.g. ("response.status_code == 200",)
