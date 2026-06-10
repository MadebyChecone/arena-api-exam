from grader.criteria._types import BehaviorCriterion

CRITERIA = [
    BehaviorCriterion(
        id="elo_formula_is_correct",
        points=4,
        file="grader/tests/logic/test_match_results_elo.py",
        function="test_elo_formula_is_correct",
        description="ELO expected score and rating updates follow the standard formula.",
    ),
    BehaviorCriterion(
        id="match_result_permissions",
        points=3,
        file="grader/tests/logic/test_match_results_elo.py",
        function="test_match_result_permissions",
        description="Only match participants and admins can record match results.",
    ),
    BehaviorCriterion(
        id="match_result_validates_inputs",
        points=3,
        file="grader/tests/logic/test_match_results_elo.py",
        function="test_match_result_validates_inputs",
        description="Result recording rejects unknown, unready, outsider, and duplicate results.",
    ),
    BehaviorCriterion(
        id="match_result_advances_and_finishes",
        points=3,
        file="grader/tests/logic/test_match_results_elo.py",
        function="test_match_result_advances_and_finishes",
        description="Results advance winners correctly and finish the tournament after the final.",
    ),
    BehaviorCriterion(
        id="match_result_updates_elo",
        points=2,
        file="grader/tests/logic/test_match_results_elo.py",
        function="test_match_result_updates_elo",
        description="Recording a result persists ELO changes for winner and loser.",
    ),
]

assert sum(c.points for c in CRITERIA) == 15
