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

    @staticmethod
    def get_orders_by_account(account):
        try:
            return Order.objects.filter(account=account).order_by('-created_date')
        except Order.DoesNotExist:
            return None

    @staticmethod
    def update_payment_status(payment_id, status):
        try:
            order = Order.objects.get(payment_id=payment_id)

            order.payment_status = status
            print('JAJAJAJAJAJ', status)
            if status == "paid":
                order.order_status = "Betaald"
            elif status == "failed":
                order.order_status = "Mislukt"
            elif status == "canceled":
                order.order_status = "Mislukt"
            elif status == "expired":
                order.order_status = "Mislukt"
            else:
                order.order_status = "Openstaand"

            order.save()
            return order
        except Order.DoesNotExist:
            return None

    @staticmethod
    def add_payment(payment, order):
        try:

            order = Order.objects.get(id=order.id)

            order.payment_id = payment['id']
            order.payment_status = payment['status']
            order.payment_url = payment['_links']['checkout']['href']

            order.save()
            return order
        except Order.DoesNotExist:
            return None
