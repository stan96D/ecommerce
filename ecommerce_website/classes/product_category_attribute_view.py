class ProductCategoryAttributeView():

    def __init__(self, product_category_attribute):
        self.id = product_category_attribute.id
        self.attribute_type_name = product_category_attribute.attribute_type.name
        self.attribute_type_id = product_category_attribute.attribute_type.id
        self.category_name = product_category_attribute.category.name
        self.category_id = product_category_attribute.category.id
        self.product_attributes = [{
            'id': attribute.id,
            'value': attribute.value
        } for attribute in product_category_attribute.attributes.all()]

    def serialize(self):
        return {
            'id': self.id,
            'attribute_type_name': self.attribute_type_name,
            'attribute_type_id': self.attribute_type_id,
            'category_name': self.category_name,
            'category_id': self.category_id,
            'product_attributes': self.product_attributes
        }


class ProductCategoryView:
    def __init__(self, product_category_attribute):
        self.id = product_category_attribute.category.id
        self.name = product_category_attribute.category.name
        self.category_attributes = [
            {
                'attribute_type_id': product_category_attribute.attribute_type.id,
                'attribute_type_name': product_category_attribute.attribute_type.name,
                'attributes': [
                    {
                        'attribute_id': attribute.id,
                        'attribute_value': attribute.value
                    }
                    for attribute in product_category_attribute.attributes.all()
                ]
            }
        ]

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'category_attributes': self.category_attributes
        }
