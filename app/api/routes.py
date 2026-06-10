from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.api.dev_support import router as dev_support_router
from app.api.matches import router as matches_router
from app.api.players import router as players_router
from app.api.tournaments import router as tournaments_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(players_router)
router.include_router(tournaments_router)
router.include_router(matches_router)


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


router.include_router(dev_support_router)
