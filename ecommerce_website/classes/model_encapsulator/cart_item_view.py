from ecommerce_website.classes.helpers.surface_area_calculator import SurfaceAreaCalculator


class CartItemView:
    def __init__(self, product, quantity):
        attributes_dict = {}
        for attribute in product.attributes.all():
            attributes_dict[attribute.attribute_type.name] = attribute.value

        self.id = product.id
        self.name = product.name
        self.price = product.selling_price
        self.unit_price = product.unit_selling_price
        self.attributes = attributes_dict

        if product.thumbnail_url:
            self.thumbnail_url = product.thumbnail_url

        else:
            self.thumbnail_url = "/static/images/no_image_placeholder.png"

        self.quantity = quantity
        self.stock = product.stock.quantity

        self.product_type = attributes_dict.get('Producttype', 'Vloer')
        self.unit = attributes_dict.get('Eenheid', 'm²')

        self.brand = attributes_dict.get('Merk', '')

        self.has_sale = str(product.has_product_sale).lower()

        if self.product_type == "Vloer":

            if product.has_product_sale:

                self.totalPrice = quantity * product.unit_sale_price
            else:
                self.totalPrice = quantity * product.unit_selling_price
        else:

            if product.has_product_sale:

                self.totalPrice = quantity * product.sale_price
            else:
                self.totalPrice = quantity * product.selling_price

        self.sale_price = product.sale_price
        self.unit_sale_price = product.unit_sale_price


class CartView:
    def __init__(self, total_price, sub_price, tax_price_high, tax_price_low, shipping_price):

        self.total_price = total_price
        self.sub_price = sub_price
        self.tax_price_high = tax_price_high
        self.tax_price_low = tax_price_low
        self.shipping_price = shipping_price
