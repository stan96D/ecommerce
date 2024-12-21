from ecommerce_website.services.view_service.base_view_service import SingleViewServiceInterface, EmptyViewServiceInterface
from ecommerce_website.classes.model_encapsulator.order_info_view import OrderInfoView


class OrderInfoViewService(SingleViewServiceInterface, EmptyViewServiceInterface):

    def get(self, item):
        productView = OrderInfoView(
            item["first_name"], item["last_name"], item["email"], item["phone"], item["address"], item["house_number"], item["city"], item["postal_code"], item["country"], item['salutation'], item["billing_address"], item["billing_house_number"], item["billing_city"], item["billing_postal_code"], item["billing_country"])
        return productView

    def get_single(self):
        productView = OrderInfoView(
            "", "", "", "", "", "", "", "", "", "Meneer", "", "", "", "", "")  # TODO fix default

        return productView
