"""ELO rating system."""

DEFAULT_K_FACTOR = 32


def compute_new_ratings(
    rating_a: int,
    rating_b: int,
    score_a: float,
    k: int = DEFAULT_K_FACTOR,
) -> tuple[int, int]:
    """Compute updated ratings for both players after a match."""
    expected_a = expected_score(rating_a, rating_b)
    expected_b = expected_score(rating_b, rating_a)

    score_b = 1 - score_a
    rating_a = rating_a + k * (score_a - expected_a)
    rating_b = rating_b + k * (score_b - expected_b)
    return round(rating_a), round(rating_b)


def expected_score(rating_a: int, rating_b: int) -> float:
    """Probability that player A beats player B given their ratings."""
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))
