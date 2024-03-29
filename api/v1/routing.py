from api.base_routing import BaseRouting

from .endpoints.create_bill import CreateBill
from .endpoints.get_bills import GetBills
from .endpoints.login_user import LoginUser
from .endpoints.register_user import RegisterUser


class RoutingV1(BaseRouting):
    api_version: str = "v1"

    def set_routing_collection(self):
        self.routing_collection[RegisterUser.api_name] = (
            RegisterUser(),
            RegisterUser.api_url,
        )
        self.routing_collection[LoginUser.api_name] = (LoginUser(), LoginUser.api_url)
        self.routing_collection[CreateBill.api_name] = (
            CreateBill(),
            CreateBill.api_url,
        )
        self.routing_collection[GetBills.api_name] = (GetBills(), GetBills.api_url)
