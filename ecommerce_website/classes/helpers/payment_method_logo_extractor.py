from abc import ABC, abstractmethod
from ecommerce_website.classes.managers.payment_manager.base_payment_manager import PaymentClient
from mollie.api.error import RequestError

class BasePaymentMethodLogoExtractor(ABC):

    @abstractmethod
    def extract():
        pass


class MolliePaymentMethodLogoExtractor(BasePaymentMethodLogoExtractor):

    def __init__(self, payment_client: PaymentClient) -> None:
        
        self.payment_client = payment_client
        

    def extract(self, method_id):
        try:
            print(method_id)
            payment_methods = self.payment_client.get_payment_methods()
            print(payment_methods)

            found_method = None

            for method in payment_methods:
                print(method.id)
                if method.id == method_id:
                    found_method = method

            if found_method:
                return found_method.image_url
            else:
                return None
        except RequestError as e:
            print('Error retrieving payment method image:', e)
            return None