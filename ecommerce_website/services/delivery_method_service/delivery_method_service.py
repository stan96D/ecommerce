from ecommerce_website.models import *


class DeliveryMethodService():

    @staticmethod
    def get_all_active_delivery_methods():
        try:
            return DeliveryMethod.objects.filter(active=True, delivery_type='delivery')
        except DeliveryMethod.DoesNotExist:
            return None

    @staticmethod
    def get_all_active_takeaway_methods():
        try:
            return DeliveryMethod.objects.filter(active=True, delivery_type='takeaway')
        except DeliveryMethod.DoesNotExist:
            return None
