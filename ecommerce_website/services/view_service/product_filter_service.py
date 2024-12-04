from ecommerce_website.services.view_service.base_view_service import ViewServiceInterface
from ecommerce_website.classes.model_encapsulator.product_filter_view import ProductFilterView


class ProductFilterViewService(ViewServiceInterface):

    def generate(self, items):
        productViews = []
        for item in items:
            productView = ProductFilterView({
                "name": item.name,
                "values": item.values,
                "filter_type": item.filter_type,
                "unit": item.unit_value,
            })

            if productView.type == 'slider':

                if productView.lowest != productView.highest:
                    productViews.append(productView)

            else:
                productViews.append(productView)

        return productViews

    def get(self, item):

        productView = ProductFilterView(item)
        return productView
