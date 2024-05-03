from mollie.api.client import Client
from mollie.api.objects.method import *
from ecommerce_website.services.view_service.payment_issuer_view_service import *
from ecommerce_website.classes.managers.payment_manager.base_payment_manager import *
import environ

env = environ.Env()


class MollieClient(PaymentClient):

    def __init__(self):
        api_key = env.str('MOLLIE_API_KEY')
        if not api_key:
            raise ValueError("MOLLIE_API_KEY environment variable is not set")

        self.api_key = api_key
        self.client = Client()
        self.client.set_api_key(api_key)


    def get_issuers(self):
        method = self.client.methods.get(
            Method.IDEAL, include='issuers')
        
        payment_issuer_service = PaymentIssuerViewService()

        payment_issuers = payment_issuer_service.generate(method["issuers"])

        return payment_issuers


    def create_payment(self, currency, amount, description, redirect_url, webhook_url, method, issuer=None):
        payment_data = {
            'amount': {
                'currency': currency,
                'value': amount
            },
            'description': description,
            'redirectUrl': redirect_url,
            'webhookUrl': webhook_url,
            'method': method
        }

        if issuer is not None:
            payment_data['issuer'] = issuer

        payment = self.client.payments.create(payment_data)
        return payment


    def get_payment(self, payment_id):
        payment = self.client.payments.get(payment_id)
        return payment

    def handle_webhook(self, payment_id):
        try:
            payment = self.get_payment(payment_id)
            # Handle the payment status update here
            # You can update the order status in your database based on the payment status
            print(f"Webhook received for payment {
                  payment_id}. Status: {payment.status}")
            return True
        except Exception as e:
            print(f"Error handling webhook: {e}")
            return False
