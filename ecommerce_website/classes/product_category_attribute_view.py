class ProductCategoryAttributeView():

    def __init__(self, product_category_attribute):
        self.attribute_type_name = product_category_attribute.attribute_type.name
        self.attribute_type_id = product_category_attribute.attribute_type.id
        self.category_name = product_category_attribute.category.name
        self.category_id = product_category_attribute.category.id
        self.product_attributes = [{
            'id': product_attribute.id,
            'value': product_attribute.value
        } for product_attribute in product_category_attribute.product_attributes.all()]
