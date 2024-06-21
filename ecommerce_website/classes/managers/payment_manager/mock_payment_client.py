from ecommerce_website.services.view_service.payment_issuer_view_service import PaymentIssuerViewService
from ecommerce_website.classes.model.payment_method import PaymentMethod
from ecommerce_website.classes.managers.payment_manager.base_payment_manager import PaymentClient
from ecommerce_website.classes.helpers.cache import Cache


class MockPaymentClient(PaymentClient):
    def __init__(self):
        self.cache = Cache()
        self.mock_methods = []
        self.mock_payments = {}
        self.mock_refunds = {}

    def get_payment_methods(self):
        cached_methods = self.cache.get('payment_methods')
        if cached_methods is not None:
            print("Using cached payment methods")
            return cached_methods

        response = {
            '_embedded': {
                'methods': [
                    {
                        'id': 'ideal',
                        'status': 'activated',
                        'description': 'iDEAL'
                    },
                    {
                        'id': 'creditcard',
                        'status': 'activated',
                        'description': 'Credit Card'
                    }
                ]
            }
        }

        installed_methods = [PaymentMethod.from_dict(
            method) for method in response['_embedded']['methods'] if method['status'] == 'activated']

        for method in installed_methods:
            issuers = self.get_issuers(method.id)
            method.add_issuers(issuers)

        self.cache.set('payment_methods', installed_methods, ttl=900)
        print("Payment methods retrieved and cached")
        return installed_methods

    def get_issuers(self, method_id):
        mock_issuers = {
            'ideal': [
                {'id': 'issuer_a', 'name': 'Issuer A'},
                {'id': 'issuer_b', 'name': 'Issuer B'}
            ],
            'creditcard': [
                {'id': 'issuer_c', 'name': 'Issuer C'}
            ]
        }

        issuers = mock_issuers.get(method_id, [])
        payment_issuer_service = PaymentIssuerViewService()
        payment_issuers = payment_issuer_service.generate(issuers)

        return payment_issuers

    def create_payment(self, currency, amount, description, redirect_url, webhook_url, method, issuer=None):
        payment_id = f"tr_{len(self.mock_payments) + 1}"
        payment_data = {
            'id': payment_id,
            'amount': {
                'currency': currency,
                'value': amount
            },
            'description': description,
            'redirectUrl': redirect_url,
            'webhookUrl': webhook_url,
            'method': method,
            'issuer': issuer,
            'status': 'paid',
            '_links': {
                'checkout': {
                    'href': 'https://example.com/checkout'
                }
            }
        }
        self.mock_payments[payment_id] = payment_data

        return payment_data

    def get_payment(self, payment_id):
        return self.mock_payments.get(payment_id, None)

    def refund_payment(self, payment_id, amount):
        if payment_id not in self.mock_payments:
            print('Error refunding payment: Payment not found')
            raise Exception('Payment not found')

        refund_id = f"rf_{len(self.mock_refunds) + 1}"
        refund_data = {
            'id': refund_id,
            'amount': {
                'value': amount,
                'currency': 'EUR'
            },
            'status': 'pending'
        }

        self.mock_refunds[refund_id] = refund_data
        return refund_data

