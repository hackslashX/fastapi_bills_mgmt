from crud.base import CRUDBase
from crud.schemas import BillItemCreate, BillItemUpdate
from models.bill_item import BillItem


class CRUDBillItem(CRUDBase[BillItem, BillItemCreate, BillItemUpdate]):
    ...


bill_item = CRUDBillItem(BillItem)
