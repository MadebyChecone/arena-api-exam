from grader.criteria._types import BehaviorCriterion

CRITERIA = [
    BehaviorCriterion(
        id="bracket_seed_players_by_elo",
        points=3,
        file="grader/tests/logic/test_bracket.py",
        function="test_bracket_seed_players_by_elo",
        description="Seeding sorts by ELO and applies the 1-vs-N pattern.",
    ),
    BehaviorCriterion(
        id="bracket_seed_tiebreak_is_deterministic",
        points=2,
        file="grader/tests/logic/test_bracket.py",
        function="test_bracket_seed_tiebreak_is_deterministic",
        description="Equal-ELO seeding is deterministic and tie-breaks by lower id.",
    ),
    BehaviorCriterion(
        id="bracket_validates_player_count",
        points=3,
        file="grader/tests/logic/test_bracket.py",
        function="test_bracket_validates_player_count",
        description="Bracket construction rejects invalid player counts.",
    ),
    BehaviorCriterion(
        id="bracket_materializes_match_tree",
        points=6,
        file="grader/tests/logic/test_bracket.py",
        function="test_bracket_materializes_match_tree",
        description="Bracket construction creates the expected match tree and empty later rounds.",
    ),
    BehaviorCriterion(
        id="bracket_wires_advancement_slots",
        points=6,
        file="grader/tests/logic/test_bracket.py",
        function="test_bracket_wires_advancement_slots",
        description="Bracket matches feed winners into the correct parent slots and persist on start.",
    ),
]

assert sum(c.points for c in CRITERIA) == 20
