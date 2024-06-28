class RelatedProductView():

    def __init__(self, related_product) -> None:

        self.name = related_product.name
        self.products = [
            {
                "id": product.id,
                "name": product.name,
                "thumbnail_url": product.thumbnail.url if product.thumbnail and product.thumbnail.url else "/static/images/no_image_placeholder.png",
                "unit_price": product.unit_sale_price if product.has_product_sale else product.unit_selling_price,
                "price": product.sale_price if product.has_product_sale else product.selling_price,
                "old_unit_price": product.unit_selling_price if product.has_product_sale else None,
                "old_price": product.selling_price if product.has_product_sale else None,
                "has_product_sale": product.has_product_sale,
            }

            for product in related_product.related_products.all()
        ]
