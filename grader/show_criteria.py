"""Pretty-print all graded criteria. Read-only: does not run pytest.

Use this to see the spec at a glance:

    python -m grader.show_criteria
"""

import sys
from collections import defaultdict
from pathlib import Path

from rich.console import Console
from rich.markup import escape
from rich.panel import Panel

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from grader.criteria import CRITERIA, BehaviorCriterion, Criterion, StudentTestCriterion


def main() -> None:
    console = Console()
    total = sum(c.points for c in CRITERIA)

    console.print(
        Panel.fit(
            f"[bold cyan]Graded criteria[/]\n[bold]{total} points total[/]",
            border_style="cyan",
            padding=(0, 2),
        )
    )

    by_category: dict[str, list[Criterion]] = defaultdict(list)
    for criterion in CRITERIA:
        by_category[criterion.category].append(criterion)

    for category, items in by_category.items():
        category_total = sum(c.points for c in items)
        console.rule(
            f"[bold cyan]{escape(category)}[/] [dim]({category_total} points)[/]"
        )
        for criterion in items:
            _print_criterion(console, criterion)
        console.print()


def _print_criterion(console: Console, criterion: Criterion) -> None:
    is_behavior = isinstance(criterion, BehaviorCriterion)
    kind = "behavior" if is_behavior else "student test"
    kind_style = "blue" if is_behavior else "magenta"

    console.print(
        f"  [bold]{escape(criterion.id)}[/] "
        f"[dim]· {criterion.points} pts ·[/] [{kind_style}]{kind}[/]"
    )
    console.print(
        f"    [dim]{escape(criterion.file)} :: {escape(criterion.function)}[/]",
        soft_wrap=True,
    )

    if is_behavior:
        console.print(f"    {escape(criterion.description)}")
    elif isinstance(criterion, StudentTestCriterion):
        _print_student_test_details(console, criterion)

    console.print()


def _print_student_test_details(
    console: Console, criterion: StudentTestCriterion
) -> None:
    if criterion.prompt:
        console.print(f"    {escape(criterion.prompt.strip())}")

    if criterion.expected_calls:
        console.print("    [bold]Must call[/]")
        for call in criterion.expected_calls:
            console.print(f"      • [cyan]{escape(call)}[/]")

    if criterion.expected_asserts:
        console.print("    [bold]Must assert[/]")
        for assertion in criterion.expected_asserts:
            console.print(f"      • [cyan]assert {escape(assertion)}[/]")


if __name__ == "__main__":
    main()
