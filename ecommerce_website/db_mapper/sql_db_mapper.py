from ecommerce_website.db_mapper.base_db_mapper import DatabaseMapperInterface


class SQLDatabaseMapper(DatabaseMapperInterface):

    def map_products(self, products_json):

        products = []
        attribute_types = []
        product_attributes = []

        for product_data in products_json:
            product = product_data['Product']
            sku = product_data['SKU']
            supplier = product_data['Leverancier']
            image = product_data['Thumbnail']
            measure_price = product_data.get(
                "Prijs", product_data["Totaalprijs"])
            unit_price = product_data['Totaalprijs']
            images = product_data["Afbeeldingen"]

            product_output = {'name': product,
                              'sku': sku,
                              'supplier': supplier,
                              'thumbnail': image,
                              'images': images,
                              'measure_price': measure_price,
                              'unit_price': unit_price,
                              "delivery_date": product_data.get("Leverdatum", None),
                              "stock": product_data.get("Voorraad", 0),
                              }

            products.append(product_output)

            for key, value in product_data.items():

                not_product_or_image = key not in [
                    'Product', 'Thumbnail', 'SKU', 'Prijs', 'Totaalprijs', 'Leverancier', 'Afbeeldingen', 'Leverdatum', 'Voorraad']

                duplicate_attribute_type = any(attribute.get(
                    'name') == key for attribute in attribute_types)

                if not_product_or_image:

                    product_attribute_type_output = {'name': key}

                    if not duplicate_attribute_type:
                        attribute_types.append(product_attribute_type_output)

                    product_attribute_output = {
                        'value': value, 'sku': sku, 'attribute_name': key}
                    product_attributes.append(product_attribute_output)

        return products, product_attributes, attribute_types
