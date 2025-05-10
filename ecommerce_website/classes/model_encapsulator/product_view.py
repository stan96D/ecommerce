from ecommerce_website.classes.helpers.surface_area_calculator import SurfaceAreaCalculator
import json


# Assuming you're using Django's cache system
from django.core.cache import cache

from ecommerce_website.settings.webshop_config import WebShopConfig


class ProductView:
    def __init__(self, product):
        # Access the prefetched attributes directly
        attributes_dict = {
            attr.attribute_type.name: attr.value
            for attr in getattr(product, 'filtered_attributes', [])
        }

        # Basic product details
        self.id = product.id
        self.name = product.name
        self.price = product.selling_price
        self.unit_price = product.unit_selling_price

        # Thumbnail handling with a fallback to a default image
        self.thumbnail_url = product.thumbnail_url if product.thumbnail_url else "/static/images/no_image_placeholder.png"

        # Accessing attributes from the pre-fetched dictionary
        self.product_type = attributes_dict.get('Producttype', 'Vloer')
        self.unit = attributes_dict.get('Eenheid', 'm²')
        self.brand = attributes_dict.get('Merk', WebShopConfig.customBrand())

        # Images and stock quantity
        self.images = product.images
        self.quantity = product.stock.quantity
        self.is_runner = product.runner

        # Sale prices, only assign if the product is on sale
        if product.has_product_sale:
            self.sale_price = product.sale_price
            self.unit_sale_price = product.unit_sale_price

        self.has_product_sale = product.has_product_sale
        # Check if the product is in the cache for favorites
        self.favorite = self.check_if_favorite()

    def check_if_favorite(self):
        """
        Check if the product is in the 'favorites' cache.
        If the product is in the cache, set the favorite attribute to True,
        otherwise set it to False.
        """
        favorites = cache.get(
            'favorites') or []  # Retrieve the list of favorite product IDs from the cache
        if str(self.id) in map(str, favorites):  # Check if the product's ID is in the favorites list
            return True
        return False


class ProductRelatedView:
    def __init__(self, product):
        self.id = product.id
        self.name = product.name

        if product.thumbnail_url:
            self.thumbnail_url = product.thumbnail_url

        else:
            self.thumbnail_url = "/static/images/no_image_placeholder.png"


class ProductDetailView:
    def __init__(self, product):
        attributes_dict = {}
        for attribute in product.attributes.all():
            attributes_dict[attribute.attribute_type.name] = attribute.value

        self.id = product.id
        self.name = product.name
        self.unit_price = product.unit_selling_price
        self.price = product.selling_price

        if product.thumbnail_url:
            self.thumbnail_url = product.thumbnail_url

        else:
            self.thumbnail_url = "/static/images/no_image_placeholder.png"

        self.product_id = product.sku
        self.images = product.images
        self.quantity = product.stock.quantity
        self.description = attributes_dict.get('Omschrijving', '')

        self.product_type = attributes_dict.get('Producttype', 'Vloer')
        self.unit = attributes_dict.get('Eenheid', 'm²')
        surface = attributes_dict.get('Verpakking', None)

        if self.product_type == "Vloer" and surface:
            self.surface = SurfaceAreaCalculator.parse_surface_area(
                surface)
            self.big_unit = "pak"
            self.big_unit_multi = "pakken"

        elif self.product_type == "Ondervloeren":
            self.big_unit = "rol"
            self.big_unit_multi = "rollen"
        else:
            self.surface = "undefined"

        self.brand = attributes_dict.get('Merk', '')
        self.has_sale = str(product.has_product_sale)

        self.sale_price = product.sale_price
        self.unit_sale_price = product.unit_sale_price

        self.active = product.active

        product_specifications = {
            "Algemene Specificaties": {},
            "Overige Specificaties": {},
            "Aanvullende Informatie": {},
            "Omschrijving": {}
        }

        for attribute in product.attributes.all():
            attribute_type = attribute.attribute_type.name
            attribute_value = attribute.value

            # Skip 'Leverancier' attribute
            if attribute_type == "Leverancier":
                continue

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

                # If links_dict is a list (array) of dictionaries, process each dictionary
                if isinstance(links_dict, list):
                    # Create a new dictionary where each element in the list (which is a dict) is added
                    # The key from each dictionary will be retained as the key.
                    # We will flatten the list of dictionaries into a single dictionary.
                    flat_dict = {}
                    for item in links_dict:
                        if isinstance(item, dict):  # Check if the item is a dictionary
                            # Add each key-value pair to the flat_dict
                            flat_dict.update(item)

                    links_dict = flat_dict  # Replace links_dict with the flattened version

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

        self.favorite = self.check_if_favorite()

    def check_if_favorite(self):
        """
        Check if the product is in the 'favorites' cache.
        If the product is in the cache, set the favorite attribute to True,
        otherwise set it to False.
        """
        favorites = cache.get(
            'favorites') or []  # Retrieve the list of favorite product IDs from the cache
        if str(self.id) in map(str, favorites):  # Check if the product's ID is in the favorites list
            return True
        return False
