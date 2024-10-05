from abc import ABC, abstractmethod
from django.conf import settings


class EncapsulatedURLManager():

    @staticmethod
    def get_url_manager(env):

        if env == "dev":
            return TestURLManager()

        elif env == "test":
            return RealURLManager()

        elif env == "prod":
            return RealURLManager()


class URLManager(ABC):

    @abstractmethod
    def get_base():
        pass

    @abstractmethod
    def get_contact_service():
        pass

    @abstractmethod
    def get_account():
        pass

    @abstractmethod
    def store_rating():
        pass

    @abstractmethod
    def create_redirect(self, currency, amount, description, redirect_url, webhook_url):
        pass

    @abstractmethod
    def create_webhook(self, currency, amount, description, redirect_url, webhook_url):
        pass


class TestURLManager(URLManager):

    @staticmethod
    def get_base():
        return settings.BASE_URL

    @staticmethod
    def get_contact_service():
        return TestURLManager.get_base()  # TODO create contact service page

    @staticmethod
    def get_account():
        return TestURLManager.get_base() + "/account"

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
    def get_base():
        return settings.BASE_URL

    @staticmethod
    def get_contact_service():
        return RealURLManager.get_base()  # TODO create contact service page

    @staticmethod
    def get_account():
        return RealURLManager.get_base() + "/account"

    @staticmethod
    def create_webhook():
        return RealURLManager.get_base() + "/mollie_webhook/"

    @staticmethod
    def create_redirect(order_id):
        return RealURLManager.get_base() + "/order_detail?order_id=" + str(order_id)

    @staticmethod
    def store_rating():
        return RealURLManager.get_base() + "/store_rating"
