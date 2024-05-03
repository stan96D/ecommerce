from mollie.api.client import Client
from mollie.api.objects.method import *

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
        method = self.client.methods.get(
            Method.IDEAL, include='issuers')
        print("All issuers!!!!; ", method)

    def create_payment(self, currency, amount, description, redirect_url, webhook_url):
        payment = self.client.payments.create({
            'amount': {
                'currency': currency,
                'value': amount
            },
            'description': description,
            'redirectUrl': redirect_url,
            'webhookUrl': webhook_url,
            'method': 'ideal'
        })
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
