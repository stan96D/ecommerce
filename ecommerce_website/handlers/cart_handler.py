from ecommerce_website.services.shopping_cart_services.shopping_cart_service import ShoppingCartService
from ecommerce_website.services.product_service.product_service import ProductService
from ecommerce_website.models import ProductAttribute
from ecommerce_website.handlers.base_handler import BaseHandlerInterface


class CartHandler(BaseHandlerInterface):

    def __init__(self, request):
        self.cart_service = ShoppingCartService(request)
        self.product_service = ProductService()

    def __get_product_attributes(self, product_ids):
        product_attributes = {}
        for product_id in product_ids:
            attributes_qs = ProductAttribute.objects.filter(product_id=product_id)
            attributes_list = list(attributes_qs)
            product_attributes[product_id] = attributes_list
        return product_attributes

    def __get_cart_items_with_attributes(self, cart_items):
        product_ids = [item['product_id'] for item in cart_items]
        product_attributes = self.__get_product_attributes(product_ids)
        for item in cart_items:
            product_id = item['product_id']
            attributes_qs = product_attributes.get(product_id, [])
            attributes_dict = {
                attr.attribute_type.name: attr.value for attr in attributes_qs
            }
            item['attributes'] = attributes_dict
        return cart_items

    @property
    def data(self):
        cart_items = self.cart_service.cart_items
        cart_items_with_attributes = self.__get_cart_items_with_attributes(cart_items)
        return cart_items_with_attributes
    