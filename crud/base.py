from typing import Any, Dict, Generic, Iterable, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import delete, exc, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
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

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        async with db as session:
            stmt = select(self.model).filter(self.model.id == id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        page: int,
        per_page: int,
        order_by: str,
        order: str,
        stmt: Optional[select] = None,
    ) -> Iterable[ModelType]:
        """
        Get multiple objects from the database.

        Args:
            db (AsyncSession): SQLAlchemy session
            page (int): The page number
            per_page (int): The number of items per page
            order_by: The column to order by
            order (str): The order to sort by

        Returns:
            Iterable[ModelType]: A list of objects
        """

        async with db as session:
            order_by = getattr(self.model, order_by, None)
            if order_by is None:
                order_by = self.model.id
            if order not in ["asc", "desc"]:
                order = "asc"
            if stmt is None:
                stmt = select(self.model)

            stmt = (
                stmt.order_by(order_by.asc() if order == "asc" else order_by.desc())
                .offset((page - 1) * per_page)
                .limit(per_page)
            )

            result = await session.execute(stmt)
            return result.all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new object in the database.

        Args:
            db (AsyncSession): SQLAlchemy session
            obj_in (CreateSchemaType): The object to create

        Returns:
            ModelType: The created object
        """

        async with db as session:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data)  # type: ignore
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        """
        Update an object in the database.

        Args:
            db (AsyncSession): SQLAlchemy session
            db_obj (ModelType): The object to update
            obj_in (Union[UpdateSchemaType, Dict[str, Any]]): The object with the new values

        Returns:
            ModelType: The updated object
        """

        async with db as session:
            obj_data = jsonable_encoder(db_obj)
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.model_dump(exclude_unset=True)
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj

    async def bulk_update(
        self, db: AsyncSession, *, db_objs: List[ModelType]
    ) -> List[ModelType]:
        """
        Update multiple objects in the database.

        Args:
            db (AsyncSession): SQLAlchemy session
            db_objs (List[ModelType]): The objects to update

        Returns:
            List[ModelType]: The updated objects
        """

        async with db as session:
            for db_obj in db_objs:
                session.add(db_obj)
            await session.commit()
            return db_objs

    async def bulk_create(
        self, db: AsyncSession, *, objs_in: CreateSchemaType
    ) -> List[ModelType]:
        """
        Create multiple objects in the database.

        Args:
            db (AsyncSession): SQLAlchemy session
            objs_in (CreateSchemaType): The objects to create

        Returns:
            List[ModelType]: The created objects
        """
        async with db as session:
            db_objs = []
            for obj_in in objs_in:
                obj_in_data = jsonable_encoder(obj_in)
                db_obj = self.model(**obj_in_data)  # type: ignore
                db_objs.append(db_obj)
                session.add(db_obj)
            await session.commit()
            return db_objs

    async def remove(self, db: AsyncSession, *, id: int):
        """
        Remove an object from the database.

        Args:
            db (AsyncSession): SQLAlchemy session
            id (int): The ID of the object to remove
        """

        async with db as session:
            stmt = delete(self.model).filter(self.model.id == id)
            await session.execute(stmt)
            await session.commit()
