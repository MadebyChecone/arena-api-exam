"""Aggregates per-category criteria into a single CRITERIA list.

Each .py file in this package (except _types.py) is one category.
The category name is derived from the module name and injected
into each criterion; never set `category` manually.

Adding a new category: create a new module here, export CRITERIA,
then append it to _MODULES below.
"""

from dataclasses import replace

from grader.criteria import (
    auth_security,
    bracket,
    match_results_elo,
    summary,
    tournament_workflow,
)
from grader.criteria._types import BehaviorCriterion, Criterion, StudentTestCriterion

__all__ = ["BehaviorCriterion", "CRITERIA", "Criterion", "StudentTestCriterion"]

_MODULES = [
    auth_security,
    tournament_workflow,
    bracket,
    match_results_elo,
    summary,
]


def _categorized(module) -> list[Criterion]:
    category = module.__name__.rsplit(".", 1)[-1]
    return [replace(c, category=category) for c in module.CRITERIA]


CRITERIA: list[Criterion] = [c for m in _MODULES for c in _categorized(m)]
