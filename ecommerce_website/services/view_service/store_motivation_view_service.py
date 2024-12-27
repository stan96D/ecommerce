from ecommerce_website.services.view_service.base_view_service import ViewServiceInterface
import json


class StoreMotivationViewService(ViewServiceInterface):

    def generate(self, items):
        productViews = []

        for item in items:
            productView = {
                'icon': item.icon,
                'name': item.name,
                'text': item.text,
                'image': item.image.url if item.image else '',
                'for_homepage': json.dumps(item.for_homepage)
            }
            productViews.append(productView)
        print(productViews)
        return productViews

    def get(self, item):
        productView = {
            'icon': item.icon,
            'name': item.name,
            'text': item.text,
            'image': item.image.url if item.image else '',
            'for_homepage': json.dumps(item.for_homepage)
        }
        return productView
