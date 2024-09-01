from abc import ABC, abstractmethod
from django.conf import settings


class URLManager(ABC):

    @abstractmethod
    def create_store_rating():
        pass

    @abstractmethod
    def create_redirect(self, currency, amount, description, redirect_url, webhook_url):
        pass

    @abstractmethod
    def create_webhook(self, currency, amount, description, redirect_url, webhook_url):
        pass


class TestURLManager(URLManager):

    @staticmethod
    def store_rating():
        return "http://localhost:8000/store_rating"

    @staticmethod
    def create_webhook():
        return f"https://{settings.NGROK_URL}/mollie_webhook/"

    @staticmethod
    def create_redirect(order_id):
        return f"https://{
            settings.NGROK_URL}/order_detail?order_id={order_id}"


class RealURLManager(URLManager):

    @staticmethod
    def create_webhook():
        return f"https://{settings.PRODUCTION_URL}/mollie_webhook/"

    @staticmethod
    def create_redirect(order_id):
        return f"https://{
            settings.PRODUCTION_URL}/order_detail?order_id={order_id}"

    @staticmethod
    def store_rating():
        pass
