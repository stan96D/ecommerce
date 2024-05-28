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
        self.thumbnail = product.thumbnail
        self.quantity = quantity
        self.stock = product.stock.quantity
        self.totalPrice = quantity * product.unit_selling_price

        surface = attributes_dict['Oppervlakte']
        self.surface = SurfaceAreaCalculator.parse_surface_area(surface)

        brand = attributes_dict['Merk']
        self.brand = brand
        
class CartView:
    def __init__(self, total_price, sub_price, tax_price_high, tax_price_low, shipping_price):

        self.total_price = total_price
        self.sub_price = sub_price
        self.tax_price_high = tax_price_high
        self.tax_price_low = tax_price_low
        self.shipping_price = shipping_price
