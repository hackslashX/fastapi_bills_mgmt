from datetime import datetime

from pydantic import BaseModel, Field


class BillItemBase(BaseModel):
    bill_id: int
    item_id: int


class BillItemCreate(BillItemBase):
    ...


class BillItemUpdate(BillItemBase):
    ...


class BillItemInDB(BillItemBase):
    id: int

    class Config:
        from_attributes = True


class BillItem(BillItemInDB):
    ...
