from typing import List
from deta import Base

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic.networks import EmailStr

import schemas
from core import deps
from core.config import settings
from utils import send_new_account_email
from users import crud

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Base = Depends(deps.get_db),
    limit: int = 2000,
    buffer: int = 100,
) -> List[schemas.User]:
    """
    Retrieve users.
    """
    users = crud.user.get_many(db, query={}, limit=limit, buffer=buffer)
    return [schemas.User(**user.dict()) for user in users]


@router.post("/", response_model=schemas.User)
def create_user(
    *,
    db: Base = Depends(deps.get_db),
    user_in: schemas.UserCreate,
) -> schemas.User:
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user is not None:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    if settings.EMAILS_ENABLED and user_in.email:
        send_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
    return schemas.User(**user.dict())


@router.post("/open", response_model=schemas.User)
def create_user_open(
    *,
    db: Base = Depends(deps.get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
    full_name: str = Body(None),
) -> schemas.User:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = crud.user.get_by_email(db, email=email)
    if user is not None:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_in = schemas.UserCreate(password=password, email=email, full_name=full_name)
    user = crud.user.create(db, obj_in=user_in)
    return schemas.User(**user.dict())


@router.get("/{user_key}", response_model=schemas.User)
def read_user_by_id(
    user_key: str,
    db: Base = Depends(deps.get_db),
) -> schemas.User:
    """
    Get a specific user by key.
    """
    user = crud.user.get(db, user_key)
    return schemas.User(**user.dict())


@router.put("/{user_key}", response_model=schemas.User)
def update_user(
    *,
    db: Base = Depends(deps.get_db),
    user_key: str,
    user_in: schemas.UserUpdate,
) -> schemas.User:
    """
    Update a user.
    """
    user = crud.user.update(db, user_key, obj_in=user_in)
    return schemas.User(**user.dict())
