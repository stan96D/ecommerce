from mollie.api.client import Client
from mollie.api.error import RequestError
from ecommerce_website.services.view_service.payment_issuer_view_service import PaymentIssuerViewService
from ecommerce_website.classes.model.payment_method import PaymentMethod
from ecommerce_website.classes.managers.payment_manager.base_payment_manager import PaymentClient
from ecommerce_website.classes.helpers.cache import Cache
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
        self.cache = Cache()  

    def get_payment_methods(self):
        cached_methods = self.cache.get('payment_methods')
        if cached_methods is not None:
            print("Using cached payment methods")
            return cached_methods

        try:
            response = self.client.methods.all()
            installed_methods = [PaymentMethod.from_dict(
                method) for method in response['_embedded']['methods'] if method['status'] == 'activated']
            for method in installed_methods:
                issuers = self.get_issuers(method.id)
                method.add_issuers(issuers)

            self.cache.set('payment_methods', installed_methods, ttl=900)
            print("Payment methods retrieved and cached")
            return installed_methods
        except RequestError as e:
            print('Error retrieving payment methods:', e)
            return []

    def get_issuers(self, method_id):
        method = self.client.methods.get(
            method_id, include='issuers')

        if 'issuers' not in method:
            return []

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
        print(payment_data)
        payment = self.client.payments.create(payment_data)
        return payment

    def get_payment(self, payment_id):
        payment = self.client.payments.get(payment_id)
        return payment
    
    def refund_payment(self, payment_id, amount):
        try:
            refund_data = {
                'amount': {
                    'value': amount,
                    'currency': 'EUR'
                }
            }

            payment = self.client.payments.get(payment_id)
            refund = payment.refunds.create(refund_data)

            return refund
        except RequestError as e:
            print('Error refunding payment:', e)
            raise e

