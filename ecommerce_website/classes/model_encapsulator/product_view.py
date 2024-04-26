
class ProductView:
    def __init__(self, product):

        print("TEXTEXTEXTETX", product.search_string)

        self.id = product.id
        self.name = product.name
        self.price = product.selling_price
        self.thumbnail = product.thumbnail
        self.images = product.images
        self.quantity = product.stock.quantity


class ProductDetailView:
    def __init__(self, product):
        attributes_dict = {}
        for attribute in product.attributes.all():
            attributes_dict[attribute.attribute_type.name] = attribute.value
        print("TEXTEXTEXTETX", product.search_string)

        self.id = product.id
        self.name = product.name
        self.price = product.selling_price
        self.attributes = attributes_dict
        self.thumbnail = product.thumbnail
        self.images = product.images
        self.quantity = product.stock.quantity
