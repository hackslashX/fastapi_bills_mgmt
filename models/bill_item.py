from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer

from db.base_class import Base


class BillItem(Base):
    """
    Represents an item in a bill.

    Attributes:
        id (int): The unique identifier for the bill item.
        bill_id (int): The ID of the bill that this item belongs to.
        item_id (int): The ID of the item associated with this bill item.
    """

    id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(Integer, ForeignKey("bill.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("item.id"), nullable=False)
