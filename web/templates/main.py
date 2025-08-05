from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from web.routes import router

app = FastAPI(title="Football Bot Dashboard")

# Mount templates & static
app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")

# Register routes
app.include_router(router)
