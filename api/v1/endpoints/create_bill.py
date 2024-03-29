from typing import List

from fastapi import status

import crud
from api.base_resource import PostResource
from common.exceptions import RequestException
from crud.schemas import Bill, BillCreate, BillItemCreate, Item, ItemCreate

from ..schemas.create_bills import CreateBillRequest, CreateBillResponse


class CreateBill(PostResource):
    # Endpoint Request and Response Schemas
    request_schema = CreateBillRequest
    response_schema = CreateBillResponse

    # Endpoint is authenticated
    authentication_required = True

    # Endpoint details
    api_name = "create_bills"
    api_url = "bills"

    async def initialize(self):
        """
        Initialize the endpoint
        """

        self.bill = None
        self.items = None

    async def create_items(self, items: List[ItemCreate]) -> List[Item]:
        """
        Create items in the database

        Args:
            items (List[ItemCreate]): List of items to create

        Returns:
            List[Item]: List of created items
        """

        created_items = await crud.item.bulk_create(self.db, objs_in=items)
        return created_items

    async def check_reference_uniqueness(self, items: List[ItemCreate]) -> None:
        """
        Check if the reference in the items is unique

        Args:
            items (List[ItemCreate]): List of items
        """

        references = [item.reference for item in items]
        existing_items = await crud.item.get_one_by_references(
            db=self.db, references=references
        )
        if existing_items:
            raise RequestException(
                "One or more references already exist in the database"
            )

    async def create_bill(self, bill: CreateBillRequest) -> Bill:
        """
        Create a bill in the database

        Args:
            bill (CreateBillRequest): The bill object

        Returns:
            Bill: The created bill object
        """

        bill_data = BillCreate(
            user_id=self.context["user"]["id"], **bill.dict(exclude={"user_id"})
        )
        created_bill = await crud.bill.create(self.db, obj_in=bill_data)
        return created_bill

    async def create_bill_items(self, bill: Bill, items: List[Item]) -> None:
        """
        Create bill items in the database

        Args:
            bill (Bill): The bill object
            items (List[Item]): List of items to create
        """

        bill_items = [
            BillItemCreate(bill_id=bill.id, item_id=item.id) for item in items
        ]
        await crud.bill_item.bulk_create(self.db, objs_in=bill_items)

    async def generate_response(self):
        """
        Generate the response for the endpoint
        """

        self.status_code = status.HTTP_200_OK
        self.response_message = "Bill created successfully"
        self.response_data = {**self.bill.to_dict(), "sub_bills": self.items}

    async def process_flow(self):
        """
        Process the flow of the endpoint
        """

        await self.check_reference_uniqueness(items=self.request_data.sub_bills)
        self.items = await self.create_items(items=self.request_data.sub_bills)
        self.bill = await self.create_bill(bill=self.request_data)
        await self.create_bill_items(bill=self.bill, items=self.items)
        await self.generate_response()
