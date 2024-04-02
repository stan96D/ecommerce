class CartItemView:
    def __init__(self, product, quantity):
        attributes_dict = {}
        for attribute in product.attributes.all():
            attributes_dict[attribute.attribute_type.name] = attribute.value
            
        self.id = product.id
        self.name = product.name
        self.price = product.price
        self.attributes = attributes_dict
        self.thumbnail = product.thumbnail
        self.quantity = quantity
        self.stock = product.stock.quantity
        self.totalPrice = quantity * product.price


class CartView:
    def __init__(self, total_price, sub_price, tax_price_high, tax_price_low):

        self.total_price = total_price
        self.sub_price = sub_price
        self.tax_price_high = tax_price_high
        self.tax_price_low = tax_price_low
