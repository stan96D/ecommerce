from django.db.models import F
from ecommerce_website.services.store_motivation_service.base_store_motivation_service import *
from ecommerce_website.models import *


class StoreMotivationService(StoreMotivationInterface):

    @staticmethod
    def get_all_motivations():
        try:
            return StoreMotivation.objects.all().order_by(F('sort_order').asc(nulls_last=True))
        except StoreMotivation.DoesNotExist:
            return None

    @staticmethod
    def get_all_active_motivations():
        try:
            return StoreMotivation.objects.filter(active=True).order_by(F('sort_order').asc(nulls_last=True))
        except StoreMotivation.DoesNotExist:
            return None
