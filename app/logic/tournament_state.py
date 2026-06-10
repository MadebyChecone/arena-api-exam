"""Tournament status state machine."""

from app.models import TournamentStatus


def validate_transition(
    current: TournamentStatus,
    target: TournamentStatus,
) -> None:
    """Validate a tournament status transition."""
    return None


def is_terminal(status: TournamentStatus) -> bool:
    """Return whether a status is terminal."""
    return False
