from abc import ABC, abstractmethod


class PaymentClient(ABC):
    @abstractmethod
    def create_payment(self, currency, amount, description, redirect_url, webhook_url):
        pass

    @abstractmethod
    def get_payment(self, payment_id):
        pass

    @abstractmethod
    def get_issuers(self):
        pass
