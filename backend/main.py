from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core.config import settings
from core.api import api_router as core
from users.api import api_router as users

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json", version=settings.VERSION
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(core)
app.include_router(users)
