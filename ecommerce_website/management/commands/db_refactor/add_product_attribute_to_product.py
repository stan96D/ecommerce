

from ecommerce_website.services.database_import_service.sql_import_service import SQLImportService
from ecommerce_website.services.product_service.product_service import ProductService


def add_product_attribute_to_product(productId=1, product_attribute_name="Lengte", new_value="55 cm"):

    service = SQLImportService()

    product = ProductService.get_product_by_id(productId)

    service.create_product_attribute(
        product, product_attribute_name, new_value)
