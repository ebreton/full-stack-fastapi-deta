from typing import Dict

from deta import Base
from fastapi.testclient import TestClient

from backend.schemas.user import User, UserCreate, UserUpdate
from backend.users import crud

from .utils import random_email, random_lower_string


def user_authentication_headers(
    *, client: TestClient, email: str, password: str
) -> Dict[str, str]:
    return {"Authorization": "Bearer fake"}


def create_random_user(db: Base) -> User:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(username=email, email=email, password=password)
    user = crud.user.create(db=db, obj_in=user_in)
    return user


def authentication_token_from_email(
    *, client: TestClient, email: str, db: Base
) -> Dict[str, str]:
    """
    Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    user = crud.user.get_by_email(db, email=email)
    if not user:
        user_in_create = UserCreate(username=email, email=email, password=password)
        user = crud.user.create(db, obj_in=user_in_create)
    else:
        user_in_update = UserUpdate(password=password)
        user = crud.user.update(db, key=user.key, obj_in=user_in_update)

    return user_authentication_headers(client=client, email=email, password=password)
