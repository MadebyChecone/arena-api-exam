from grader.criteria._types import BehaviorCriterion

CRITERIA = [
    BehaviorCriterion(
        id="auth_passwords_are_hashed",
        points=4,
        file="grader/tests/api/test_auth_security.py",
        function="test_auth_passwords_are_hashed",
        description="Registered passwords are stored as verifiable hashes, not plaintext.",
    ),
    BehaviorCriterion(
        id="auth_register_cannot_create_admin",
        points=4,
        file="grader/tests/api/test_auth_security.py",
        function="test_auth_register_cannot_create_admin",
        description="Registration cannot create an admin account through request data.",
    ),
    BehaviorCriterion(
        id="auth_responses_do_not_leak_passwords",
        points=4,
        file="grader/tests/api/test_auth_security.py",
        function="test_auth_responses_do_not_leak_passwords",
        description="Auth and player responses do not expose password fields.",
    ),
    BehaviorCriterion(
        id="auth_protected_reads_require_token",
        points=4,
        file="grader/tests/api/test_auth_security.py",
        function="test_auth_protected_reads_require_token",
        description="Protected read endpoints require a bearer token.",
    ),
    BehaviorCriterion(
        id="auth_admin_required_for_tournament_creation",
        points=4,
        file="grader/tests/api/test_auth_security.py",
        function="test_auth_admin_required_for_tournament_creation",
        description="Only admins can create tournaments.",
    ),
]

assert sum(c.points for c in CRITERIA) == 20
