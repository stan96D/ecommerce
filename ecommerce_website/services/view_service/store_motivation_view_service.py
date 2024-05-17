from ecommerce_website.services.view_service.base_view_service import ViewServiceInterface
import json

class StoreMotivationViewService(ViewServiceInterface):

    def generate(self, items):
        productViews = []

        for item in items:
            productView = {
                'name': item.name,  
                'text': item.text,
                'image': item.image.url if item.image else '',
                'for_homepage': json.dumps(item.for_homepage)
            }
            productViews.append(productView)

        return productViews

    def get(self, item):
        productView = {
            'name': item.name,
            'text': item.text,
            'image': item.image.url if item.image else '',
            'for_homepage': json.dumps(item.for_homepage)
        }
        return productView
