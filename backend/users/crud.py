from typing import Any, Dict, Optional, Union

from deta import Base

from core.security import get_password_hash, verify_password
from core.crud import CRUDBase
from schemas.user import UserCreate, UserUpdate, UserInDB, User


class CRUDUser(CRUDBase[UserInDB, UserCreate, UserUpdate]):
    def get_by_email(self, db: Base, *, email: str) -> Optional[UserInDB]:
        users = next(db.fetch({"email": email}))
        if len(users) == 0:
            return None
        if len(users) > 1:
            raise ValueError(f"More than one user with given email {email}")
        return UserInDB(**users[0])

    def create(self, db: Base, *, obj_in: UserCreate) -> UserInDB:
        db_obj = {
            'email': obj_in.email,
            'hashed_password': get_password_hash(obj_in.password),
            'full_name': obj_in.full_name,
            'is_superuser': obj_in.is_superuser,
        }
        return UserInDB(**db.put(db_obj))

    def update(
        self, db: Base, *, key: str, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> None:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        super(CRUDUser, self).update(db, key, obj_in=update_data)

    def authenticate(self, db: Base, *, email: str, password: str) -> Optional[UserInDB]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(UserInDB)
