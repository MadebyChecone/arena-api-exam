"""Sync instructor metadata.

Two responsibilities:
1. For each grader/criteria/<category>.py: update the `assert sum(...) == N`
   line from the sum of `points=` in CRITERIA.
2. Recompute EXPECTED_FILE_HASHES in grader/engine/reviewed_files.py.

Run this after editing any instructor-owned file.
"""

import ast
import hashlib
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from grader.engine.reviewed_files import INSTRUCTOR_OWNED_PATHS

CRITERIA_DIR = PROJECT_ROOT / "grader" / "criteria"
REVIEWED_FILES = PROJECT_ROOT / "grader" / "engine" / "reviewed_files.py"

EXCLUDED_RELATIVES = {"grader/engine/reviewed_files.py"}
EXCLUDED_PARTS = {"__pycache__", ".pytest_cache"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def main() -> None:
    print("Syncing criteria totals...")
    update_criteria_totals()
    print("\nUpdating instructor file hashes...")
    update_review_hashes()


# -- 1. criteria totals --------------------------------------------------------


def update_criteria_totals() -> None:
    for path in sorted(CRITERIA_DIR.glob("*.py")):
        if path.name in {"__init__.py", "_types.py"}:
            continue
        total = _criteria_total(path)
        if total is None:
            print(f"  {path.relative_to(PROJECT_ROOT)}: no CRITERIA found, skipped")
            continue
        _rewrite_total(path, total)
        print(f"  {path.relative_to(PROJECT_ROOT)}: total = {total}")


def _criteria_total(path: Path) -> int | None:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(t, ast.Name) and t.id == "CRITERIA" for t in node.targets):
            continue
        if not isinstance(node.value, ast.List):
            return 0
        total = 0
        for elt in node.value.elts:
            if not isinstance(elt, ast.Call):
                continue
            for keyword in elt.keywords:
                if keyword.arg == "points" and isinstance(keyword.value, ast.Constant):
                    total += keyword.value.value
        return total
    return None


def _rewrite_total(path: Path, total: int) -> None:
    content = path.read_text(encoding="utf-8")
    content = re.sub(
        r"assert sum\(c\.points for c in CRITERIA\) == \d+",
        f"assert sum(c.points for c in CRITERIA) == {total}",
        content,
    )
    path.write_text(content, encoding="utf-8")


# -- 2. instructor file hashes -------------------------------------------------


def update_review_hashes() -> None:
    hashes: dict[str, str] = {}
    for owned in INSTRUCTOR_OWNED_PATHS:
        path = PROJECT_ROOT / owned
        candidates = sorted(path.rglob("*")) if owned.endswith("/") else [path]
        for f in candidates:
            if not f.is_file():
                continue
            relative = f.relative_to(PROJECT_ROOT).as_posix()
            if (
                relative in EXCLUDED_RELATIVES
                or f.suffix in EXCLUDED_SUFFIXES
                or any(p in EXCLUDED_PARTS for p in f.parts)
            ):
                continue
            hashes[relative] = hashlib.sha256(f.read_bytes()).hexdigest()

    body = "EXPECTED_FILE_HASHES: dict[str, str] = {\n"
    for name in sorted(hashes):
        body += f'    "{name}": "{hashes[name]}",\n'
    body += "}\n"

    content = REVIEWED_FILES.read_text(encoding="utf-8")
    new = re.sub(
        r"EXPECTED_FILE_HASHES: dict\[str, str\] = \{[^}]*\}\n",
        body,
        content,
        count=1,
    )
    REVIEWED_FILES.write_text(new, encoding="utf-8")
    print(f"  {REVIEWED_FILES.relative_to(PROJECT_ROOT)}: {len(hashes)} hashes")


if __name__ == "__main__":
    main()
