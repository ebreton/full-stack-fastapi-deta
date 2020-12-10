from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from deta import Base, Deta

from backend.core.config import settings
from backend.main import app

from .utils.user import authentication_token_from_email
from .utils.utils import get_superuser_token_headers


@pytest.fixture(scope="session")
def db() -> Generator:
    return Deta(settings.PROJECT_KEY).Base(settings.TEST_DB_NAME)


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> Dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Base) -> Dict[str, str]:
    return authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db
    )
