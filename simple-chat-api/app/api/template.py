from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from settings import BASE_DIR

api = APIRouter()
template_engine = Jinja2Templates(
    directory=f"{BASE_DIR}/app/asset")
templating = template_engine.TemplateResponse


@api.get(
    '/',
    summary="Welcome to Simple-Chat-API",
    tags=['template'],
)
async def index(request: Request):
    return templating("index.html", {"request": request})
