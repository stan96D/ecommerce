from ecommerce_website.services.store_motivation_service.base_store_motivation_service import *
from ecommerce_website.models import *

class StoreMotivationService(StoreMotivationInterface):

    @staticmethod
    def get_all_motivations():
        try:
            return StoreMotivation.objects.all()
        except Order.DoesNotExist:
            return None
        
    @staticmethod
    def get_all_active_motivations():
        try:
            return StoreMotivation.objects.filter(active=True)
        except Order.DoesNotExist:
            return None
