from fastapi import APIRouter

from core.config import settings

from .api_v1.endpoints import router

api_router = APIRouter()
api_router.include_router(router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
