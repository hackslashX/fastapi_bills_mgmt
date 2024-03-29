from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.exceptions import RequestDBException
from crud.base import CRUDBase
from crud.schemas import ItemCreate, ItemUpdate
from models.item import Item


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    async def bulk_create(
        self, db: AsyncSession, *, objs_in: List[ItemCreate]
    ) -> List[Item]:
        """
        Create multiple items in the database.

        Args:
            db (AsyncSession): SQLAlchemy session
            objs_in (List[ItemCreate]): The items to create

        Returns:
            List[Item]: The created items
        """

        try:
            return await super().bulk_create(db, objs_in=objs_in)
        except Exception:
            raise RequestDBException("Unique constraint failed on reference.")

    async def get_one_by_references(
        self, db: AsyncSession, *, references: List[str]
    ) -> List[Item]:
        """
        Get items by references.

        Args:
            db (AsyncSession): SQLAlchemy session
            references (List[str]): List of references

        Returns:
            List[Item]: List of items
        """

        async with db as session:
            stmt = select(self.model.id).filter(self.model.reference.in_(references)).limit(1)
            result = await session.execute(stmt)
            return result.scalars().one_or_none()


item = CRUDItem(Item)
