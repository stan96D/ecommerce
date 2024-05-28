from ecommerce_website.db_mapper.base_db_mapper import DatabaseMapperInterface


class SQLDatabaseMapper(DatabaseMapperInterface):

    def map_products(self, products_json):

        products = []
        attribute_types = []
        product_attributes = []

        for product_data in products_json:
            product = product_data['Product']
            image = product_data['Thumbnail']
            measure_price = product_data['Prijs per m2']
            unit_price = product_data['Prijs per pak']

            if 'Afbeeldingen' in product_data:
                images = product_data['Afbeeldingen']
                images.append(image)
            else:
                images = [image]

            product_output = {'name': product,
                'thumbnail': image,
                'images': images,
                              'measure_price': measure_price,
                              'unit_price': unit_price}
            
            products.append(product_output)

            for key, value in product_data.items():

                not_product_or_image = key not in [
                    'Product', 'Thumbnail', 'Prijs per m2', 'Prijs per pak', 'Afbeeldingen']

                duplicate_attribute_type = any(attribute.get('name') == key for attribute in attribute_types)

                if not_product_or_image:

                    product_attribute_type_output = {'name': key}

                    if not duplicate_attribute_type:
                        attribute_types.append(product_attribute_type_output)

                    product_attribute_output = {'value': value, 'product_name': product, 'attribute_name': key}
                    product_attributes.append(product_attribute_output)

        return products, product_attributes, attribute_types
    



