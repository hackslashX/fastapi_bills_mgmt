from typing import List

from pydantic import model_validator

from crud.schemas import Bill, BillCreate, Item, ItemCreate


class CreateBillRequest(BillCreate):
    sub_bills: List[ItemCreate]
    user_id: None = None

    @model_validator(mode="after")
    @classmethod
    def total_must_be_sum_of_items(cls, v, values, **kwargs):
        """
        Validate that the total is the sum of all sub_bills
        """

        items = v.sub_bills
        if not items:
            total = 0
            return v

        total = sum([item.amount for item in items])
        if total != v.total:
            raise ValueError("total must be the sum of all sub_bills")
        return v

    @model_validator(mode="after")
    @classmethod
    def reference_must_be_unique(cls, v, values, **kwargs):
        """
        Validate that the reference is unique in all sub_bills
        """

        references = set()
        for item in v.sub_bills:
            if item.reference in references:
                raise ValueError("reference must be unique")
            references.add(item.reference)
        return v


class CreateBillResponse(Bill):
    sub_bills: List[Item]
