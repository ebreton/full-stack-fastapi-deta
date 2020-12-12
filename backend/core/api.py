import sys
import fastapi
import pydantic

from fastapi import APIRouter

from core.config import settings


api_router = APIRouter()


@api_router.get('/')
@api_router.get('/version')
def version():
    return {
        "application": settings.VERSION,
        "python": sys.version,
        "fastapi": fastapi.__version__,
        "pydantic": pydantic.version.VERSION,
        "api": f"{settings.SERVER_HOST}{settings.API_V1_STR}/users",
        "swagger": f"{settings.SERVER_HOST}/docs",
        "redoc": f"{settings.SERVER_HOST}/redoc",
    }