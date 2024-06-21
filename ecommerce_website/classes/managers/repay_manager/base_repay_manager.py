from abc import ABC, abstractmethod
from ecommerce_website.classes.managers.payment_manager.mollie_client import MollieClient
from ecommerce_website.services.order_service.base_order_service import OrderServiceInterface

class RepayManagerInterface(ABC):

    @abstractmethod
    def repay(order_id, order_service: OrderServiceInterface):
        pass



