
class ProductView:
    def __init__(self, product):
        self.id = product.id
        self.name = product.name
        self.price = product.price
        self.attributes = product.attributes
        self.thumbnail = product.thumbnail
        self.images = product.images
        self.quantity = product.stock.quantity

