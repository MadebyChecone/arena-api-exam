import json
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections import defaultdict
from html import escape as html_escape
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from grader.criteria import CRITERIA, Criterion, StudentTestCriterion
from grader.engine.ast_checks import check_student_test
from grader.engine.reviewed_files import modified_instructor_files

RESULTS_PATH = PROJECT_ROOT / "grading-results.json"
SUMMARY_PATH = PROJECT_ROOT / "grading-summary.md"


def score(criteria: list[Criterion]) -> dict:
    """Pure: run all criteria and return the result dict."""
    results = run_criteria(criteria)
    max_score = sum(c.points for c in criteria)
    total = sum(r["score"] for r in results)
    modified = modified_instructor_files()

    return {
        "score": total,
        "max_score": max_score,
        "mark_20": round(total / max_score * 20, 2) if max_score else 0.0,
        "categories": category_totals(results),
        "criteria": results,
        "review": {
            "status": "needs_review" if modified else "clean",
            "modified_instructor_files": modified,
        },
    }


def main() -> int:
    result = score(CRITERIA)
    summary = render_summary(result)
    RESULTS_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    SUMMARY_PATH.write_text(summary, encoding="utf-8")
    print(summary, end="")
    return 0  # CI always succeeds; the score itself is the signal.


def render_summary(result: dict) -> str:
    lines = [
        f"# Grading: {result['score']} / {result['max_score']} "
        f"({result['mark_20']} / 20)",
        "",
        "## Category scores",
        "",
        "| Category | Score |",
        "| --- | ---: |",
    ]

    for category, totals in result["categories"].items():
        lines.append(
            f"| `{_md_cell(category)}` | {totals['score']} / {totals['max_score']} |"
        )

    lines += [
        "",
        "## Criteria",
        "",
        "| Status | Criterion | Category | Score |",
        "| --- | --- | --- | ---: |",
    ]
    for criterion in result["criteria"]:
        icon = "✅" if criterion["status"] == "passed" else "❌"
        status = "Passed" if criterion["status"] == "passed" else "Failed"
        lines.append(
            f"| {icon} {status} | `{_md_cell(criterion['id'])}` | "
            f"`{_md_cell(criterion['category'])}` | "
            f"{criterion['score']} / {criterion['max_score']} |"
        )

    failed = [c for c in result["criteria"] if c["status"] != "passed"]
    if failed:
        lines += ["", "## Failed criteria details", ""]
        for criterion in failed:
            lines += _failure_details(criterion)

    if result["review"]["status"] != "clean":
        lines += ["", "## Manual review required", ""]
        lines.append("Instructor-owned files were modified:")
        lines.append("")
        for filename in result["review"]["modified_instructor_files"]:
            lines.append(f"- `{filename}`")

    lines += [
        "",
        "---",
        "",
        f"**Final score:** {result['score']} / {result['max_score']} "
        f"({result['mark_20']} / 20)",
        "",
        f"JSON results written to `{RESULTS_PATH.relative_to(PROJECT_ROOT)}`.",
    ]
    return "\n".join(lines) + "\n"


def _failure_details(criterion: dict) -> list[str]:
    summary = (
        f"❌ <code>{html_escape(criterion['id'])}</code> "
        f"({criterion['score']} / {criterion['max_score']})"
    )
    lines = ["<details>", f"<summary>{summary}</summary>", ""]

    if criterion["description"]:
        lines += [f"**Expected:** {criterion['description']}", ""]

    if criterion["details"]:
        fence = _code_fence_for(criterion["details"])
        lines += ["**Details:**", "", f"{fence}text", criterion["details"], fence, ""]

    lines += ["</details>", ""]
    return lines


def _md_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def _code_fence_for(text: str) -> str:
    fence = "```"
    while fence in text:
        fence += "`"
    return fence


def run_criteria(criteria: list[Criterion]) -> list[dict]:
    ast_results: dict[str, dict] = {}
    pytest_criteria: list[Criterion] = []

    for criterion in criteria:
        if isinstance(criterion, StudentTestCriterion):
            ast_ok, problems = check_student_test(criterion)
            if not ast_ok:
                ast_results[criterion.id] = _result(
                    criterion,
                    passed=False,
                    details="; ".join(problems),
                )
                continue

        pytest_criteria.append(criterion)

    pytest_outcomes = _run_pytest(pytest_criteria)
    results = []
    for criterion in criteria:
        if criterion.id in ast_results:
            results.append(ast_results[criterion.id])
            continue

        passed, details = pytest_outcomes.get(
            criterion.nodeid,
            (False, "pytest did not report this criterion"),
        )
        results.append(_result(criterion, passed=passed, details=details))

    return results


def run_criterion(criterion: Criterion) -> dict:
    """Run one criterion. Kept for small tests/debugging; grading uses batching."""
    return run_criteria([criterion])[0]


def _result(criterion: Criterion, passed: bool, details: str) -> dict:
    return {
        "id": criterion.id,
        "type": type(criterion).__name__,
        "category": criterion.category,
        "score": criterion.points if passed else 0,
        "max_score": criterion.points,
        "status": "passed" if passed else "failed",
        "description": getattr(criterion, "description", ""),
        "details": details,
    }


def _run_pytest(criteria: list[Criterion]) -> dict[str, tuple[bool, str]]:
    if not criteria:
        return {}

    with tempfile.TemporaryDirectory() as tmpdir:
        report_path = Path(tmpdir) / "pytest.xml"
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "-q",
                "--tb=line",
                "--no-header",
                f"--junitxml={report_path}",
                *(criterion.nodeid for criterion in criteria),
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=PROJECT_ROOT,
        )
        return _read_pytest_outcomes(report_path, criteria, completed.stdout)


def _read_pytest_outcomes(
    report_path: Path,
    criteria: list[Criterion],
    pytest_output: str,
) -> dict[str, tuple[bool, str]]:
    fallback = pytest_output.strip() or "pytest did not report this criterion"
    if not report_path.exists():
        return {criterion.nodeid: (False, fallback) for criterion in criteria}

    try:
        root = ET.parse(report_path).getroot()
    except ET.ParseError:
        return {criterion.nodeid: (False, fallback) for criterion in criteria}

    by_test = _outcomes_by_test(root, fallback)
    return {
        criterion.nodeid: by_test.get(_junit_key(criterion), (False, fallback))
        for criterion in criteria
    }


def _outcomes_by_test(
    root: ET.Element,
    fallback: str,
) -> dict[tuple[str, str], tuple[bool, str]]:
    outcomes: dict[tuple[str, str], tuple[bool, str]] = {}

    for testcase in root.iter("testcase"):
        classname = testcase.attrib.get("classname", "")
        name = testcase.attrib.get("name", "").split("[", 1)[0]
        key = (classname, name)
        failure = next(
            (child for child in testcase if child.tag in {"failure", "error"}),
            None,
        )
        outcome = (
            False,
            _junit_failure_details(failure, fallback),
        ) if failure is not None else (True, "pytest passed")
        outcomes[key] = _merge_outcomes(outcomes.get(key), outcome)

    return outcomes


def _merge_outcomes(
    current: tuple[bool, str] | None,
    new: tuple[bool, str],
) -> tuple[bool, str]:
    if current is None:
        return new
    if current[0] and new[0]:
        return current
    details = [details for passed, details in (current, new) if not passed and details]
    return False, "\n\n".join(details)


def _junit_key(criterion: Criterion) -> tuple[str, str]:
    classname = criterion.file.removesuffix(".py").replace("/", ".")
    return classname, criterion.function


def _junit_failure_details(element: ET.Element, fallback: str) -> str:
    message = element.attrib.get("message", "").strip()
    text = (element.text or "").strip()
    if message and text and message not in text:
        return f"{message}\n\n{text}"
    return text or message or fallback


def category_totals(results: list[dict]) -> dict[str, dict[str, int]]:
    totals: dict[str, dict[str, int]] = defaultdict(lambda: {"score": 0, "max_score": 0})
    for result in results:
        totals[result["category"]]["score"] += result["score"]
        totals[result["category"]]["max_score"] += result["max_score"]
    return dict(totals)


def print_report(result: dict) -> None:
    print(render_summary(result), end="")


if __name__ == "__main__":
    raise SystemExit(main())
