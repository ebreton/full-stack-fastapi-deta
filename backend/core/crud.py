from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from deta import Base
from pydantic import BaseModel

InDbSchemaType = TypeVar("InDbSchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[InDbSchemaType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, schema: Type[InDbSchemaType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `schema`: A Pydantic model (schema) class
        """
        self.schema = schema

    def get(self, db: Base, key: str,) -> Optional[InDbSchemaType]:
        return self.schema(**db.get(key))

    def get_many(
        self,
        db: Base,
        *,
        query: Union[List[Dict[str, Any]], Dict[str, Any]],
        buffer: int = 10,
        pages: int = 100,
    ) -> List[InDbSchemaType]:
        """ Default pagination will return a maximum of 100 pages, with 10 elements each"""
        # TODO: implement pagination
        return [
            self.schema(**result)
            for result in next(db.fetch(query=query, buffer=buffer, pages=pages))
        ]

    def create(self, db: Base, *, key: str, obj_in: CreateSchemaType,) -> InDbSchemaType:
        return self.schema(**db.put(obj_in.dict(), key=key))

    def safe_create(
        self, db: Base, *, key: str, obj_in: CreateSchemaType,
    ) -> InDbSchemaType:
        return self.schema(**db.insert(obj_in.dict(), key=key))

    def create_many(
        self, db: Base, *, objs_in=List[CreateSchemaType],
    ) -> List[InDbSchemaType]:
        return [
            self.schema(**result)
            for result in db.put_many([obj_in.dict() for obj_in in objs_in])
        ]

    def update(
        self, db: Base, key: str, *, obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> None:
        if hasattr(obj_in, 'dict'):
            obj_in = obj_in.dict()
        db.update(obj_in, key=key)

    def delete(self, db: Base, *, key: str,) -> None:
        db.delete(key)
