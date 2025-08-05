from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from utils.states import games, game_states

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="web/templates")

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "games": games,
        "tournaments": game_states
    })
