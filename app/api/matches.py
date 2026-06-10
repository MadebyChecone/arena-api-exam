from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.api.auth import CurrentUser
from app.database import SessionDep
from app.logic.tournament import record_result
from app.models import Match

router = APIRouter(prefix="/matches", tags=["matches"])


class RecordResultRequest(BaseModel):
    winner_id: int


@router.post("/{match_id}/result", response_model=Match)
def record_result_endpoint(
    match_id: int,
    body: RecordResultRequest,
    session: SessionDep,
    current_user: CurrentUser,
) -> Match:
    match = session.get(Match, match_id)
    if match is None:
        raise HTTPException(status_code=404, detail="Match not found")

    participants = {match.player_a_id, match.player_b_id}
    if body.winner_id not in participants:
        raise HTTPException(status_code=400, detail="Winner must be a participant in the match")
    
    if not current_user.is_admin and current_user.id not in participants:
        raise HTTPException(status_code=403, detail="Only participants or admins can record match results")
    try:
        return record_result(session, match_id, body.winner_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
