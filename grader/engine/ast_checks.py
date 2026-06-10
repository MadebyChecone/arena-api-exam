import ast
from pathlib import Path

from grader.criteria import StudentTestCriterion

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def check_student_test(
    criterion: StudentTestCriterion,
    project_root: Path = PROJECT_ROOT,
) -> tuple[bool, list[str]]:
    path = project_root / criterion.file

    if not path.exists():
        return False, [_missing_file_message(criterion)]

    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError as error:
        return False, [_syntax_error_message(criterion, error)]

    function = _find_function(tree, criterion.function)
    if function is None:
        return False, [_missing_function_message(criterion)]

    # ast.unparse canonicalises quotes, spacing, and harmless parentheses, so a
    # literal substring match works robustly without per-style escape hatches.
    body = ast.unparse(function)
    problems: list[str] = []

    for expected in criterion.expected_calls:
        if _normalize(expected) not in body:
            problems.append(_missing_call_message(criterion, expected))

    for expected in criterion.expected_asserts:
        if f"assert {_normalize(expected)}" not in body:
            problems.append(_missing_assertion_message(criterion, expected))

    return not problems, problems


def _location(criterion: StudentTestCriterion) -> str:
    return f"{criterion.file}::{criterion.function}"


def _task_hint(criterion: StudentTestCriterion) -> str:
    if not criterion.prompt:
        return "Run `make criteria` to see all required lines for this test."
    return (
        "Task reminder from `make criteria`:\n"
        + _indent(criterion.prompt.strip(), spaces=4)
    )


def _missing_file_message(criterion: StudentTestCriterion) -> str:
    return (
        f"Missing test file: {criterion.file}\n\n"
        f"Student-test criterion `{criterion.id}` expects this file to exist.\n"
        f"Create `{criterion.file}` and add a test function named "
        f"`{criterion.function}`.\n\n"
        f"{_task_hint(criterion)}"
    )


def _syntax_error_message(
    criterion: StudentTestCriterion,
    error: SyntaxError,
) -> str:
    return (
        f"Syntax error in {criterion.file}: {error}\n\n"
        f"Fix the Python syntax before this criterion can be checked.\n"
        f"Location: {_location(criterion)}"
    )


def _missing_function_message(criterion: StudentTestCriterion) -> str:
    return (
        f"Missing test function: {criterion.function}\n\n"
        f"Student-test criterion `{criterion.id}` expects a test at:\n"
        f"    {_location(criterion)}\n\n"
        f"Add a function with this exact name:\n"
        f"    def {criterion.function}(...):\n\n"
        f"{_task_hint(criterion)}"
    )


def _missing_call_message(
    criterion: StudentTestCriterion,
    expected: str,
) -> str:
    return (
        f"Missing expected call: {expected}\n\n"
        f"Student-test criterion `{criterion.id}` failed for:\n"
        f"    {_location(criterion)}\n\n"
        f"Your test must contain a call equivalent to:\n"
        f"    {_normalize(expected)}\n\n"
        f"Add the setup/assignment you need around that call, then run "
        f"`make grade` again.\n\n"
        f"{_task_hint(criterion)}"
    )


def _missing_assertion_message(
    criterion: StudentTestCriterion,
    expected: str,
) -> str:
    return (
        f"Missing expected assertion: assert {expected}\n\n"
        f"Student-test criterion `{criterion.id}` failed for:\n"
        f"    {_location(criterion)}\n\n"
        f"Add an assertion equivalent to:\n"
        f"    assert {_normalize(expected)}\n\n"
        f"The variable names in your test must match the expression you assert. "
        f"Then run `make grade` again.\n\n"
        f"{_task_hint(criterion)}"
    )


def _indent(text: str, spaces: int) -> str:
    prefix = " " * spaces
    return "\n".join(f"{prefix}{line}" for line in text.splitlines())


def _find_function(tree: ast.AST, name: str) -> ast.FunctionDef | ast.AsyncFunctionDef | None:
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
            return node
    return None


def _normalize(expression: str) -> str:
    """Parse and unparse so the expected string matches ast.unparse style."""
    return ast.unparse(ast.parse(expression, mode="eval"))
