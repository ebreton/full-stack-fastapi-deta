from deta import Base
from fastapi.testclient import TestClient

from backend.core.config import settings
from backend.schemas.user import UserCreate
from backend.users import crud
from tests.utils.utils import random_email, random_lower_string


def test_create_user_new_email(
    client: TestClient, superuser_token_headers: dict, db: Base
) -> None:
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=superuser_token_headers, json=data,
    )
    assert 200 <= r.status_code < 300
    created_user = r.json()
    user = crud.user.get_by_email(db, email=username)
    assert user
    assert user.email == created_user["email"]
    # cleaning time ...
    crud.user.delete(db, key=user.key)


def test_get_existing_user(
    client: TestClient, superuser_token_headers: dict, db: Base
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.user.create(db, obj_in=user_in)
    user_key = user.key
    r = client.get(
        f"{settings.API_V1_STR}/users/{user_key}", headers=superuser_token_headers,
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = crud.user.get_by_email(db, email=username)
    assert existing_user
    assert existing_user.email == api_user["email"]
    # cleaning time ...
    crud.user.delete(db, key=user.key)


def test_create_user_existing_username(
    client: TestClient, superuser_token_headers: dict, db: Base
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.user.create(db, obj_in=user_in)
    data = {"email": username, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=superuser_token_headers, json=data,
    )
    created_user = r.json()
    assert r.status_code == 400
    assert "_id" not in created_user
    # cleaning time ...
    crud.user.delete(db, key=user.key)


def test_retrieve_users(
    client: TestClient, superuser_token_headers: dict, db: Base
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.user.create(db, obj_in=user_in)

    username2 = random_email()
    password2 = random_lower_string()
    user_in2 = UserCreate(email=username2, password=password2)
    user2 = crud.user.create(db, obj_in=user_in2)

    r = client.get(f"{settings.API_V1_STR}/users/", headers=superuser_token_headers)
    all_users = r.json()

    assert len(all_users) > 1
    for item in all_users:
        assert "email" in item
    # cleaning time ...
    crud.user.delete(db, key=user.key)
    crud.user.delete(db, key=user2.key)
