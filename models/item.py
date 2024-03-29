from datetime import datetime

from sqlalchemy import DECIMAL, TIMESTAMP, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import CITEXT

from db.base_class import Base


class Item(Base):
    """
    Represents an item that can be added to a bill.

    Attributes:
        id (int): The unique identifier for the item.
        name (str): The name of the item.
        price (float): The price of the item.
    """

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(DECIMAL(10, 2), nullable=False, default="0.00")
    reference = Column(CITEXT(255), nullable=True, unique=True)
