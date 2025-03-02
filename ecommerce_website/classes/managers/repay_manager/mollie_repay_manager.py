from ecommerce_website.classes.helpers.env_loader import EnvLoader
from ecommerce_website.classes.managers.payment_manager.mollie_client import MollieClient
from ecommerce_website.classes.managers.url_manager.url_manager import EncapsulatedURLManager
from ecommerce_website.services.order_service.base_order_service import OrderServiceInterface
from ecommerce_website.classes.managers.repay_manager.base_repay_manager import RepayManagerInterface
from django.conf import settings


class MollieRepayManager(RepayManagerInterface):

    def repay(self, order_id, order_service: OrderServiceInterface):

        environment = EnvLoader.get_env()
        url_manager = EncapsulatedURLManager.get_url_manager(environment)

        order = order_service.get_order_by_id(order_id)

        payment_method = order.payment_information_id
        issuer_id = order.payment_issuer

        webhook_url = url_manager.create_webhook()
        redirect_url = url_manager.create_redirect(order.token)

        payment = MollieClient().create_payment('EUR', str(
            order.total_price), order.order_number, redirect_url, webhook_url, payment_method, issuer_id)

        order_service.add_payment(payment, order)

        order_service.update_payment_status(
            payment['id'], "Open")

        return payment['_links']['checkout']['href']
