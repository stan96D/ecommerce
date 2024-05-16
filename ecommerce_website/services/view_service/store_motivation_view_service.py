from ecommerce_website.services.view_service.base_view_service import ViewServiceInterface


class StoreMotivationViewService(ViewServiceInterface):

    def generate(self, items):
        productViews = []

        for item in items:
            productView = {
                'name': item.name,  
            }
            productViews.append(productView)

        return productViews

    def get(self, item):
        productView = {
            'name': item.name,  
        }
        return productView
