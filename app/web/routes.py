from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

WEB_DIR = Path(__file__).resolve().parent

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory=WEB_DIR / "templates")


@router.get("/", response_class=HTMLResponse)
def web_home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "index.html")


@router.get("/login", response_class=HTMLResponse)
def web_login(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "login.html")


@router.get("/tournaments/{tournament_id}", response_class=HTMLResponse)
def web_tournament_detail(request: Request, tournament_id: int) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "tournament.html",
        {"tournament_id": tournament_id},
    )
