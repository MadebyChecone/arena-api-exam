"""ELO rating system."""

DEFAULT_K_FACTOR = 32


def compute_new_ratings(
    rating_a: int,
    rating_b: int,
    score_a: float,
    k: int = DEFAULT_K_FACTOR,
) -> tuple[int, int]:
    """Compute updated ratings for both players after a match."""
    return rating_a, rating_b


def expected_score(rating_a: int, rating_b: int) -> float:
    """Probability that player A beats player B given their ratings."""
    return 0.0
