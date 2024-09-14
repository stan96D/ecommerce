
class ProductFilterView:
    def __init__(self, product_filter_name, data):

        self.name = product_filter_name
        self.product_attributes = data['values']
        self.type = data['filter_type']
