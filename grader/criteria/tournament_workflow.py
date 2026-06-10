from grader.criteria._types import BehaviorCriterion

CRITERIA = [
    BehaviorCriterion(
        id="tournament_creation_validates_bracket_size",
        points=4,
        file="grader/tests/logic/test_tournament_workflow.py",
        function="test_tournament_creation_validates_bracket_size",
        description="Tournament creation accepts only power-of-2 sizes of at least 4 players.",
    ),
    BehaviorCriterion(
        id="registration_enforces_roster_rules",
        points=4,
        file="grader/tests/logic/test_tournament_workflow.py",
        function="test_registration_enforces_roster_rules",
        description="Registration rejects unknown records, duplicates, and full rosters.",
    ),
    BehaviorCriterion(
        id="registration_enforces_player_availability",
        points=4,
        file="grader/tests/logic/test_tournament_workflow.py",
        function="test_registration_enforces_player_availability",
        description="Registration locks player availability and rejects unavailable players.",
    ),
    BehaviorCriterion(
        id="registration_permissions_self_or_admin",
        points=4,
        file="grader/tests/api/test_tournament_workflow.py",
        function="test_registration_permissions_self_or_admin",
        description="Regular users register only themselves; admins can register any player.",
    ),
    BehaviorCriterion(
        id="state_machine_enforces_action_states",
        points=5,
        file="grader/tests/logic/test_tournament_workflow.py",
        function="test_state_machine_enforces_action_states",
        description="Tournament actions are allowed only in valid lifecycle states.",
    ),
    BehaviorCriterion(
        id="cancellation_transitions_and_frees_players",
        points=4,
        file="grader/tests/api/test_tournament_workflow.py",
        function="test_cancellation_transitions_and_frees_players",
        description="Cancellation enforces permissions/transitions and frees registered players.",
    ),
]

assert sum(c.points for c in CRITERIA) == 25
