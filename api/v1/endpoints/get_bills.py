from typing import List, Dict

from fastapi import status

import crud
from api.base_resource import GetResource
from common.exceptions import RequestException
from crud.schemas import Bill, BillCreate, BillItemCreate, Item, ItemCreate

from ..schemas.get_bills import BillWithItems, GetBillsRequest, GetBillsResponse


class GetBills(GetResource):
    # Endpoint Request and Response Schemas
    request_schema = GetBillsRequest
    response_schema = GetBillsResponse

    # Endpoint is authenticated
    authentication_required = True

    # Endpoint details
    api_name = "get_bills"
    api_url = "bills"

    async def initialize(self):
        """
        Initialize the endpoint
        """

        self.bills_with_items = None

    async def get_bills_with_items(self, query_data: GetBillsRequest) -> List:
        """
        Get bills with items

        Args:
            query_data (GetBillsRequest): Query parameters

        Returns:
            List: List of bills with items
        """

        bills_with_items = await crud.bill.get_bills_with_items(
            db=self.db,
            user_id = self.context["user"]["id"],
            total_from=query_data.total_from,
            total_to=query_data.total_to,
            reference=query_data.reference,
            page=query_data.page,
            per_page=query_data.per_page,
            order_by=query_data.order_by,
            order=query_data.order,
        )
        return bills_with_items or []
    
    async def format_bill_with_items(self, bills_with_items: List) -> List:
        """
        Format bills with items

        Args:
            bills_with_items (List): List of bills with items
        
        Returns:
            List: List of formatted bills with items
        """

        formatted_data = {}
        for bill_id, total, reference, amount in bills_with_items:
            if bill_id not in formatted_data:
                formatted_data[bill_id] = {
                    "id": bill_id,
                    "total": total,
                    "sub_bills": []
                }
            formatted_data[bill_id]["sub_bills"].append({
                "reference": reference,
                "amount": amount
            })
        
        return list(formatted_data.values())
    
    async def generate_response(self):
        """
        Generate the response for the endpoint
        """

        self.status_code = status.HTTP_200_OK
        self.response_message = "Bills retrieved successfully"
        self.response_data = {
            "bills": self.bills_with_items,
            "page": self.request_data.page
        }

    async def process_flow(self):
        """
        Process the flow of the endpoint
        """

        self.bills_with_items = await self.get_bills_with_items(query_data=self.request_data)
        self.bills_with_items = await self.format_bill_with_items(bills_with_items=self.bills_with_items)
        await self.generate_response()
