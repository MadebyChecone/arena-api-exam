from random import choice

from fastapi import APIRouter, Query
from pydantic import BaseModel

router = APIRouter(tags=["Developer Support"])

SKILL_ISSUE_FIXES = (
    "read the stack trace",
    "write the test you were afraid of",
    "stop debugging by vibes",
    "add one print, then remove seven",
)

SKILL_ISSUE_VERDICTS = (
    "yesterday is not a test environment",
    "your machine is not production",
    "the tests have receipts",
    "excuse logged; root cause unchanged",
)

ORACLE_ANSWERS = (
    "Accepted answer from 2013 no longer works.",
    "Marked as duplicate, but the duplicate is also closed.",
    "The stack trace already told you. You merely refused the prophecy.",
    "Have you tried deleting the cache and your expectations?",
    "Your bug is hiding between lines 1 and production.",
    "The tests are not toxic. They are emotionally available requirements.",
)

RUBBER_DUCK_THERAPIES = (
    "Explain it line by line. You will find the bug halfway through.",
    "Say the variable name out loud and feel the shame leave your body.",
    "Describe what should happen, then compare it to what your code actually says.",
    "Before touching the code, reproduce it once without panicking.",
    "Quack once for syntax, twice for logic, three times for database migrations.",
)


class SkillIssueResponse(BaseModel):
    diagnosis: str
    severity: str
    recommended_fix: str
    verdict: str | None = None


class OracleResponse(BaseModel):
    question: str
    oracle: str
    answer: str
    confidence: str


class RubberDuckResponse(BaseModel):
    duck: str
    therapy: str
    billable_hours: int
    problem: str | None = None


@router.get(
    "/skill-issue",
    summary="Diagnose the root cause of your failing code",
    response_model=SkillIssueResponse,
    response_model_exclude_none=True,
)
def skill_issue(
    excuse: str | None = Query(
        default=None,
        description="Optional excuse. Try: it worked yesterday",
    ),
) -> dict[str, str]:
    response = {
        "diagnosis": "skill issue",
        "severity": choice(("minor", "critical", "terminal but recoverable")),
        "recommended_fix": choice(SKILL_ISSUE_FIXES),
    }
    if excuse:
        response["verdict"] = choice(SKILL_ISSUE_VERDICTS)
    return response


@router.get(
    "/oracle",
    summary="Ask the ancient Stack Overflow oracle",
    response_model=OracleResponse,
)
def oracle(
    question: str = Query(
        default="why are my tests failing",
        description="The question you probably should have pasted into the stack trace first.",
    ),
) -> dict[str, str]:
    return {
        "question": question,
        "oracle": "Marked as duplicate.",
        "answer": choice(ORACLE_ANSWERS),
        "confidence": choice(
            ("vibes", "suspiciously high", "ask again after refactor")
        ),
    }


@router.get(
    "/rubber-duck",
    summary="Receive premium debugging therapy from a duck",
    response_model=RubberDuckResponse,
    response_model_exclude_none=True,
)
def rubber_duck(
    problem: str | None = Query(
        default=None,
        description="Optional bug confession. Try: my endpoint returns 500",
    ),
) -> dict[str, str | int]:
    response: dict[str, str | int] = {
        "duck": choice(("quack", "aggressive quack", "judgemental silence")),
        "therapy": choice(RUBBER_DUCK_THERAPIES),
        "billable_hours": 0,
    }
    if problem:
        response["problem"] = problem
    return response
