from datetime import datetime

from decimal import Decimal
from pydantic import BaseModel, Field


class BillBase(BaseModel):
    total: Decimal = Field(..., gt=0, decimal_places=2)


class BillCreate(BillBase):
    user_id: int
    ...


class BillUpdate(BillBase):
    ...


class BillInDB(BillBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Bill(BillInDB):
    ...
