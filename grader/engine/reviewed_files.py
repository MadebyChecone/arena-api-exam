import hashlib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Students edit only `app/`. Everything else is instructor-owned and protected.
# The whole grading system lives under `grader/`; the shared pytest fixtures live
# in the root `conftest.py`; CI lives in `.github/`.
INSTRUCTOR_OWNED_PATHS = [
    ".github/",
    "AGENTS.md",
    "CLAUDE.md",
    "conftest.py",
    "grader/",
]

# Filled with hashes of instructor-owned files that should not change.
# reviewed_files.py itself is intentionally excluded to avoid self-referential hashes.
EXPECTED_FILE_HASHES: dict[str, str] = {
    ".github/workflows/tests.yml": "5017a19074ef530e90efaef0c7120e6d06bcd7e8c103dd694cf6432fa96a45cc",
    "AGENTS.md": "5ae3ef12ca180ee338c40aeb4a5801c005d9347064692f2e3235a53435fc61d3",
    "CLAUDE.md": "918b1c90559355ef78f33fdf3562f2b021ef8bdfd8a5c8415e5decd44934de55",
    "conftest.py": "5302103d3394821767e9b31cc6a62413b2004e689e4d99616205f718c1dcf1b0",
    "grader/__init__.py": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "grader/criteria/__init__.py": "5470ec8220ae31d02db28b3c7cf9287f02d50ae29781d09e993536269369f8d2",
    "grader/criteria/_types.py": "0c36c2fe2aca470011f85c9f8a4be64cad23b2aaff65fa2a344f0c844b6d24fb",
    "grader/criteria/auth_security.py": "ecb0280e9e9626ab63e8741811e9020aa6beafd70fb10a161c71036a845926b1",
    "grader/criteria/bracket.py": "80d075b1f819fc62512aa71614ba2a84593bb0e2d884b8e9c5b7c2c7e8949c24",
    "grader/criteria/match_results_elo.py": "013c66998677fe71abbfaaf47a7754619672fc958dd64b1871c4235f77da465c",
    "grader/criteria/summary.py": "1fbf6dcbaebaae73eadb16993e603833d5284ed735d4545ff35e4224d77e13ae",
    "grader/criteria/tournament_workflow.py": "801a4c1930b974478846fcc4b9fd04ad7b4d28a5803bb0c3ab67bfa5c8a3ba8b",
    "grader/engine/__init__.py": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "grader/engine/ast_checks.py": "88537502c7f38125045a80e9ef3165b8fb72469f6e4e19a64631592ef32fce00",
    "grader/engine/run.py": "d1e88df5da810f6b070d534898e66d3d6a12ee25aaf86a39887b42f1e950bc67",
    "grader/helpers/__init__.py": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "grader/helpers/matches.py": "824f97b45a2c16fba453e1ae27ddee41726f9c4f597ee96f5551443ac861b46b",
    "grader/helpers/players.py": "49f2cc22aad8214800b722bc940706926936e6588bef8344bc0b1794fdd046eb",
    "grader/helpers/tournaments.py": "f4b18fa5f39825418e4b9a4a2ae95ab8913703432701ccda757de720703c7afc",
    "grader/show_criteria.py": "b081c08609d87eccaefac6585334d171275090dabe19f4bbd54fd763a187d816",
    "grader/sync.py": "8efa76253dc4543cec89259d1be8d4216f19ff45ed51f13e65be7e3d7155ca5a",
    "grader/tests/__init__.py": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "grader/tests/api/__init__.py": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "grader/tests/api/test_auth_security.py": "830701d25916435f6d173730f90a2174716c96cf0b474902f064555044bf834f",
    "grader/tests/api/test_summary.py": "965601de3d5b9c2cb6a8c48da856260097ad6d7fc5a1d13cd7e2addf78ff04ff",
    "grader/tests/api/test_tournament_workflow.py": "be683d8b55e8fb852aff540c7584f8ed849e797afde67c9dfbccb3073a6e6c7d",
    "grader/tests/logic/__init__.py": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "grader/tests/logic/test_bracket.py": "776624a226fbb63d6bdd6b2aacbee8d3e2415d7caa14ce5742b9426706d81c86",
    "grader/tests/logic/test_match_results_elo.py": "9d99c4f751787f3d512878819284f988e0b4afed8b655d2cbcd366f9f60f660d",
    "grader/tests/logic/test_summary.py": "4e7fac2fb30a0a40d8fd977e24b255e51742b0685079f8e4b242b726562a12f2",
    "grader/tests/logic/test_tournament_workflow.py": "dd26cefc248ea8b41c875891b80e155e3f13889a8f5e8382562f9d157e18e969",
    "grader/tests/system/__init__.py": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "grader/tests/system/test_ast_checks.py": "46188622ce67368870a9ed653adf8e7cbcf5738e4a99f662df699f424520a11e",
}


def modified_instructor_files() -> list[str]:
    return [
        filename
        for filename, expected in EXPECTED_FILE_HASHES.items()
        if not (PROJECT_ROOT / filename).exists()
        or hashlib.sha256((PROJECT_ROOT / filename).read_bytes()).hexdigest()
        != expected
    ]
