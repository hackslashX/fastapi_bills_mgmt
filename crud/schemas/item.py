from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    reference: str = Field(None, max_length=255)


class ItemCreate(ItemBase):
    ...


class ItemUpdate(ItemBase):
    ...


class ItemInDB(ItemBase):
    id: int

    class Config:
        from_attributes = True


class Item(ItemInDB):
    ...
