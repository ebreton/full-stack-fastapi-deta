from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel
from deta import Base

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(
        self, db: Base, id: str,
    ) -> Optional[ModelType]:
        return db.get(id)

    def get_many(
        self, db: Base, *, query: Union[List[Dict[str, Any]], Dict[str, Any]], limit: int = 2000, buffer: int = 100,
    ) -> List[ModelType]:
        return db.fetch(query=query, limit=limit, buffer=buffer)

    def create(
        self, db: Base, *, id: str, obj_in: CreateSchemaType,
    ) -> ModelType:
        return db.put(obj_in, id=id)

    def safe_create(
        self, db: Base, *, id: str, obj_in: CreateSchemaType,
    ) -> ModelType:
        return db.insert(obj_in, id=id)

    def create_many(
        self, db: Base, *, objs_in=List[CreateSchemaType],
    ) -> List[ModelType]:
        return db.put_many(objs_in)

    def update(
        self, db: Base, id: str, *, obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        return db.update(obj_in, id=id)

    def delete(
        self, db: Base, *, id: str,
    ) -> None:
        db.delete(id)
