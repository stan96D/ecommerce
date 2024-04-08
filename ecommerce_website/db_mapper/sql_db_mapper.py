from ecommerce_website.db_mapper.base_db_mapper import DatabaseMapperInterface


class SQLDatabaseMapper(DatabaseMapperInterface):

    def map_products(self, products_json):

        products = []
        attribute_types = []
        product_attributes = []

        for product_data in products_json:
            product = product_data['Product']
            image = product_data['Afbeelding']

            product_output = {'name': product,
                'thumbnail': image}
            
            products.append(product_output)

            for key, value in product_data.items():

                not_product_or_image = key not in ['Product', 'Afbeelding']

                duplicate_attribute_type = any(attribute.get('name') == key for attribute in attribute_types)

                if not_product_or_image:

                    product_attribute_type_output = {'name': key}

                    if not duplicate_attribute_type:
                        attribute_types.append(product_attribute_type_output)

                    product_attribute_output = {'value': value, 'product_name': product, 'attribute_name': key}
                    product_attributes.append(product_attribute_output)

        return products, product_attributes, attribute_types
    



