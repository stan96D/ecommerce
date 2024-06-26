from ecommerce_website.services.view_service.base_view_service import ViewServiceInterface
from ecommerce_website.classes.model_encapsulator.related_products_view import RelatedProductView


class RelatedProductViewService(ViewServiceInterface):

    def generate(self, items):
        relatedViews = []
        for item in items:
            relatedView = RelatedProductView(item)
            relatedViews.append(relatedView)

        return relatedViews

    def get(self, item):
        relatedView = RelatedProductView(item)
        return relatedView
