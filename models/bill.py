from datetime import datetime

from sqlalchemy import DECIMAL, TIMESTAMP, Column, ForeignKey, Integer, String

from db.base_class import Base


class Bill(Base):
    """
    Represents a bill.

    Attributes:
        id (int): The unique identifier for the bill.
        user_id (int): The ID of the user that created the bill.
        total (float): The total amount of the bill.
        created_at (datetime): The date and time the bill was created.
        updated_at (datetime): The date and time the bill was last updated.
    """

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    total = Column(DECIMAL(10, 2), nullable=False, default="0.00")

    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        TIMESTAMP, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
