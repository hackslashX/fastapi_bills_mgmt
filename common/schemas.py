from enum import StrEnum

from pydantic import BaseModel, Field


class OrderType(StrEnum):
    asc = "asc"
    desc = "desc"


class PaginatedRequest(BaseModel):
    page: int = Field(1, ge=1)
    per_page: int = Field(10, ge=10, le=20)
    order_by: str = "id"
    order: OrderType = OrderType.asc
