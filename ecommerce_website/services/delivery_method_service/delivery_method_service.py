from ecommerce_website.models import *

class DeliveryMethodService():

    @staticmethod
    def get_all_active_delivery_methods():
        try:
            return DeliveryMethod.objects.filter(active=True)
        except DeliveryMethod.DoesNotExist:
            return None
