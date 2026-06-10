from grader.criteria._types import BehaviorCriterion, StudentTestCriterion

CRITERIA = [
    StudentTestCriterion(
        id="summary_student_tests_pending",
        points=4,
        file="app/tests/logic/test_summary.py",
        function="test_summary_for_pending_tournament",
        prompt=(
            "Write a logic-layer test for a pending tournament summary. "
            "Create a full tournament that has not started, call tournament_summary(...), "
            "then check the main tournament data, zero match counters, active players, "
            "and that the tournament is not complete."
        ),
        expected_calls=(
            "tournament_summary(session, tournament.id)",
        ),
        expected_asserts=(
            "summary.status == TournamentStatus.PENDING",
            "summary.matches_played == 0",
            "summary.matches_remaining == 0",
            "len(summary.active_players) == 4",
            "summary.is_complete is False",
        ),
    ),
    StudentTestCriterion(
        id="summary_student_tests_in_progress",
        points=4,
        file="app/tests/logic/test_summary.py",
        function="test_summary_after_first_round_results",
        prompt=(
            "Write a logic-layer test for an in-progress tournament summary. "
            "Start a tournament, record the first-round results, call "
            "tournament_summary(...), then check the current round, played/remaining matches, "
            "and the players who are still active."
        ),
        expected_calls=(
            "start_tournament(session, tournament.id)",
            "record_result(session, match.id, winner_id=match.player_a_id)",
            "tournament_summary(session, tournament.id)",
        ),
        expected_asserts=(
            "summary.current_round == 2",
            "summary.matches_played == 2",
            "summary.matches_remaining == 1",
            "len(summary.active_players) == 2",
            "summary.is_complete is False",
        ),
    ),
    BehaviorCriterion(
        id="summary_logic_pending_and_unknown",
        points=4,
        file="grader/tests/logic/test_summary.py",
        function="test_summary_logic_pending_and_unknown",
        description="Pending tournament summaries are correct and unknown tournaments fail cleanly.",
    ),
    BehaviorCriterion(
        id="summary_logic_progress_and_active_players",
        points=4,
        file="grader/tests/logic/test_summary.py",
        function="test_summary_logic_progress_and_active_players",
        description="In-progress summaries report progress and active players correctly.",
    ),
    BehaviorCriterion(
        id="summary_endpoint_finished_response",
        points=4,
        file="grader/tests/api/test_summary.py",
        function="test_summary_endpoint_finished_response",
        description="The summary endpoint returns required fields for a finished tournament.",
    ),
]

assert sum(c.points for c in CRITERIA) == 20
