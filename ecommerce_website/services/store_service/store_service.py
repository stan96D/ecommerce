from django.forms.models import model_to_dict
from ecommerce_website.models import Store


class StoreService:
    @staticmethod
    def get_active_store():
        # Retrieve the first active store
        # Get the first active store
        return Store.objects.filter(active=True).first()
