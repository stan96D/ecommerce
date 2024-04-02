from ecommerce_website.models import Order
from ecommerce_website.services.order_service.base_order_service import OrderServiceInterface


class OrderService(OrderServiceInterface):
    @staticmethod
    def get_order_by_id(order_id):
        try:
            return Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return None

    @staticmethod
    def get_all_orders():
        try:
            return Order.objects.all()
        except Order.DoesNotExist:
            return None


