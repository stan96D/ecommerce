
class ProductView:
    def __init__(self, product):
        self.product_id = product.id
        self.name = product.name
        self.price = product.price
        self.attributes = product.attributes
        self.image = product.image
        self.quantity = product.stock.quantity

