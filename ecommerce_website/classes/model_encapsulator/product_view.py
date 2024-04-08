
class ProductView:
    def __init__(self, product):
        attributes_dict = {}
        for attribute in product.attributes.all():
            attributes_dict[attribute.attribute_type.name] = attribute.value

        self.id = product.id
        self.name = product.name
        self.price = product.price
        self.attributes = attributes_dict
        print(product.thumbnail)
        self.thumbnail = product.thumbnail
        self.images = product.images
        self.quantity = product.stock.quantity

