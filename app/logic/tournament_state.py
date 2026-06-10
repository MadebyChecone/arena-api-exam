"""Tournament status state machine."""

from app.models import TournamentStatus

VALID_TRANSITIONS = {
    TournamentStatus.PENDING: {
        TournamentStatus.IN_PROGRESS,
        TournamentStatus.CANCELLED,
    },
    TournamentStatus.IN_PROGRESS: {
        TournamentStatus.FINISHED,
        TournamentStatus.CANCELLED,
    },
    TournamentStatus.FINISHED: set(),
    TournamentStatus.CANCELLED: set(),
}

def validate_transition(
    current: TournamentStatus,
    target: TournamentStatus,
) -> None:
    """Validate a tournament status transition."""
    allowed_targets = VALID_TRANSITIONS.get(current, set())

    if target not in allowed_targets:
        raise ValueError(f"invalid tournament status transition from {current} to {target}")


def is_terminal(status: TournamentStatus) -> bool:
    """Return whether a status is terminal."""
    return status in {
        TournamentStatus.FINISHED,
        TournamentStatus.CANCELLED,
    }
