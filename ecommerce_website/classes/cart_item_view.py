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
