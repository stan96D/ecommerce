from ecommerce_website.services.view_service.base_view_service import ViewServiceInterface
from ecommerce_website.classes.model_encapsulator.delivery_method_view import DeliveryMethodView


class DeliveryMethodViewService(ViewServiceInterface):

    def generate(self, items):
        delivery_method_views = []

        for item in items:
            delivery_method_view = DeliveryMethodView(item)
            delivery_method_views.append(delivery_method_view)

        return delivery_method_views

    def get(self, item):
        delivery_method_view = DeliveryMethodView(item)
        return delivery_method_view
