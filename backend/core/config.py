import os
import secrets
import toml
from typing import Any, Dict, List, Optional, Union

from dotenv import load_dotenv
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, validator

# load .env in order to get SETTINGS_FILE available to os.getenv
load_dotenv()

# load project toml, especially for the version
poetry_toml = toml.load('pyproject.toml')


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    VERSION: str = poetry_toml['tool']['poetry']['version']

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_HOST: str = "localhost"
    SERVER_PORT: int = 3000
    SERVER_URL: AnyHttpUrl = f"http://{SERVER_HOST}:{SERVER_PORT}"
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True, allow_reuse=True)
    def assemble_cors_origins(
        cls, v: Union[str, List[str]]  # noqa: F841
    ) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str
    PROJECT_KEY: str
    DB_NAME: str
    SENTRY_DSN: Optional[HttpUrl] = None

    @validator("SENTRY_DSN", pre=True, allow_reuse=True)
    def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:  # noqa: F841
        if len(v) == 0:
            return None
        return v

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    @validator("EMAILS_FROM_NAME", allow_reuse=True)
    def get_project_name(
        cls, v: Optional[str], values: Dict[str, Any]  # noqa: F841
    ) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "backend/email-templates/build"
    EMAILS_ENABLED: bool = False

    @validator("EMAILS_ENABLED", pre=True, allow_reuse=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:  # noqa: F841
        return bool(
            values.get("EMAILS_ENABLED")
            and values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )

    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str
    USERS_OPEN_REGISTRATION: bool = False

    class Config:
        case_sensitive = True
        env_file = os.getenv("SETTINGS_FILE") or '.env'


settings = Settings()
