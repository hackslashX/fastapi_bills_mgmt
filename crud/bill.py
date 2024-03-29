from typing import List, Optional

from sqlalchemy import select

from crud.base import CRUDBase
from crud.schemas import BillCreate, BillUpdate
from models.bill import Bill
from models.item import Item
from models.bill_item import BillItem


class CRUDBill(CRUDBase[Bill, BillCreate, BillUpdate]):
    async def get_bills_with_items(
        self,
        db,
        *,
        user_id: int,
        total_from: Optional[int] = None,
        total_to: Optional[int] = None,
        reference: Optional[str] = None,
        page: int = 1,
        per_page: int = 10,
        order_by: str = "bill.id",
        order: str = "asc",
    ) -> Optional[List]:
        """
        Get bills with items

        Args:
            db (AsyncSession): SQLAlchemy session
            total_from (Optional[int]): Filter by total from
            total_to (Optional[int]): Filter by total to
            reference (Optional[str]): Filter by reference

        Returns:
            Optional[List]: List of bills with items
        """

        stmt = select(self.model.id, self.model.total, Item.reference, Item.amount)

        # Join on bill_item and item
        stmt = stmt.join(BillItem, BillItem.bill_id == self.model.id)
        stmt = stmt.join(Item, BillItem.item_id == Item.id)

        # Perform filtering
        stmt = stmt.where(self.model.user_id == user_id)
        if total_from:
            stmt = stmt.filter(self.model.total >= total_from)
        if total_to:
            stmt = stmt.filter(self.model.total <= total_to)
        if reference:
            stmt = stmt.filter(Item.reference.like(f"%{reference}%"))

        # Forward to get_multi
        return await self.get_multi(
            db=db,
            stmt=stmt,
            page=page,
            per_page=per_page,
            order_by=order_by,
            order=order,
        )


bill = CRUDBill(Bill)
