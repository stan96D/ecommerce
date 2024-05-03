from ecommerce_website.services.view_service.base_view_service import ViewServiceInterface
from ecommerce_website.classes.managers.payment_manager.payment_issuer import PaymentIssuer


class PaymentIssuerViewService(ViewServiceInterface):

    def generate(self, items):
        payment_issuers = []
        for item in items:

            payment_issuer = PaymentIssuer.from_dict(item)
            payment_issuers.append(payment_issuer)

        return payment_issuers

    def get(self, item):

        payment_issuer = PaymentIssuer.from_dict(item)
        return payment_issuer
