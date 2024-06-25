from ecommerce_website.classes.helpers.surface_area_calculator import SurfaceAreaCalculator
import json 

class ProductView:
    def __init__(self, product):

        attributes_dict = {}
        for attribute in product.attributes.all():
            attributes_dict[attribute.attribute_type.name] = attribute.value

        self.id = product.id
        self.name = product.name
        self.price = product.selling_price
        self.unit_price = product.unit_selling_price

        if product.thumbnail and product.thumbnail.url:
            self.thumbnail_url = product.thumbnail.url

        else:
            self.thumbnail_url = "/static/images/no_image_placeholder.png"

        self.product_type = attributes_dict.get('Producttype', 'Vloer')
        self.unit = attributes_dict.get('Eenheid', 'm²')

        self.images = product.images
        self.quantity = product.stock.quantity
        self.is_runner = product.runner

        self.brand = attributes_dict.get('Merk', '')

        if product.has_product_sale:
            self.sale_price = product.sale_price
            self.unit_sale_price = product.unit_sale_price


class ProductDetailView:
    def __init__(self, product):
        attributes_dict = {}
        for attribute in product.attributes.all():
            attributes_dict[attribute.attribute_type.name] = attribute.value

        self.id = product.id
        self.name = product.name
        self.unit_price = product.unit_selling_price
        self.price = product.selling_price

        if product.thumbnail and product.thumbnail.url:
            self.thumbnail_url = product.thumbnail.url

        else:
            self.thumbnail_url = "/static/images/no_image_placeholder.png"
        
        self.images = product.images
        self.quantity = product.stock.quantity
        self.description = attributes_dict.get('Omschrijving', '')


        self.product_type = attributes_dict.get('Producttype', 'Vloer')
        self.unit = attributes_dict.get('Eenheid', 'm²')
        surface = attributes_dict.get('Oppervlakte', None)

        if self.product_type == "Vloer" and surface:
            self.surface = SurfaceAreaCalculator.parse_surface_area(
                surface)
        else:
            self.surface = "undefined"
            

        self.brand = attributes_dict.get('Merk', '')
        self.has_sale = str(product.has_product_sale).lower()

        self.sale_price = product.sale_price
        self.unit_sale_price = product.unit_sale_price

        product_specifications = {
            "Algemene Specificaties": {},
            "Overige Specificaties": {},
            "Aanvullende Informatie": {},
            "Omschrijving": {}
        }

        for attribute in product.attributes.all():
            attribute_type = attribute.attribute_type.name
            attribute_value = attribute.value

            if attribute_type in ["Afmeting", "Totale Dikte", "Pakinhoud", "Oppervlakte", "Naam", "Type", "Collectie", "Kleur", "Merk", "Vloertype"]:
                product_specifications["Algemene Specificaties"][attribute_type] = attribute_value
            elif attribute_type in ["Omschrijving"]:
                product_specifications["Omschrijving"][attribute_type] = attribute_value

            elif attribute_type in ["Links"]:
                try:
                    links_dict = json.loads(attribute_value)
                except json.JSONDecodeError:
                    attribute_value = attribute_value.replace("'", '"')
                    links_dict = json.loads(attribute_value)

                product_specifications["Aanvullende Informatie"] = links_dict
            else:
                product_specifications["Overige Specificaties"][attribute_type] = attribute_value

            self.sections = [
                {"Omschrijving": product_specifications["Omschrijving"]},

                {"Algemene Specificaties":
                    product_specifications["Algemene Specificaties"]},

                {"Overige Specificaties":
                    product_specifications["Overige Specificaties"]},
                {"Aanvullende Informatie":
                    product_specifications["Aanvullende Informatie"]},
            ]




