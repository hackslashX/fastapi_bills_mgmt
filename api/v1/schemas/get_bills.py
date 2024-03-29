from typing import List, Optional
from pydantic import BaseModel, model_validator

from common.schemas import PaginatedRequest
from crud.schemas import BillBase, ItemBase


class GetBillsRequest(PaginatedRequest):
    total_from: Optional[float] = None
    total_to: Optional[float] = None
    reference: str = None
    pass

    @model_validator(mode="after")
    @classmethod
    def total_from_must_be_less_than_total_to(cls, v, values, **kwargs):
        """
        Validate that total_from is less than total_to
        """

        total_from = v.total_from
        total_to = v.total_to
        if total_from is not None and total_to is not None and total_from > total_to:
            raise ValueError("total_from must be less than total_to")
        return v


class BillWithItems(BillBase):
    sub_bills: List[ItemBase]


class GetBillsResponse(BaseModel):
    bills: List[BillWithItems]
    page: int
