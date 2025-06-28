from ecommerce_website.models import Product
from ecommerce_website.services.export_service.base_export_service import BaseExportService


class GoogleMerchantExportService(BaseExportService):
    def __init__(self, queryset=None):
        queryset = queryset or Product.objects.filter(active=True)
        super().__init__(queryset)

    def process_record(self, product):
        """
        Maps internal product model fields to Google Merchant Spreadsheet fields.
        """

        # Get the description value, or use a default empty string if not found
        description = next(
            (attr.value for attr in product.attributes.filter(
                attribute_type__name="Omschrijving")),
            ""
        )

        # Get the description value, or use a default empty string if not found
        brand = next(
            (attr.value for attr in product.attributes.filter(
                attribute_type__name="Merk")),
            "BaseFloor"
        )

        # Get the description value, or use a default empty string if not found
        color = next(
            (attr.value for attr in product.attributes.filter(
                attribute_type__name="Kleur")),
            ""
        )

        # Get the description value, or use a default empty string if not found
        unit = next(
            (attr.value for attr in product.attributes.filter(
                attribute_type__name="Eenheid")),
            "")

        return {
            "id": product.id,  # Vereist - Unieke ID
            "title": product.name,  # Vereist - Productnaam
            # Vereist - Max 200 chars
            "description": description,
            "availability": "in_stock" if product.stock and product.stock.quantity > 0 else "out_of_stock",  # Vereist
            "link": f"https://goedkoopstevloerenshop.nl/product/{product.id}",
            "image link": product.thumbnail_url,  # Vereist - Main image
            # Vereist - Incl currency
            "price": f"{product.selling_price:.2f} EUR",
            # Optioneel
            "sale price": f"{product.sale_price:.2f} EUR" if product.sale_price else "",
            # Vereist - Most products should have identifiers
            "identifier exists": "no",
            # Vereist - Most products should have identifiers
            "gtin": "",
            "brand": brand,  # Vereist,
            "product detail": product.search_string,
            "condition": "new",  # Vereist if not new/used/refurb
            "adult": "no",  # Vereist if adult content
            "color": color,  # Vereist for clothing
            "size": "",  # Vereist for clothing
            "gender": "",  # Vereist for clothing
            # Vereist for clothing
            "material": getattr(product, "material", ""),
            "pattern": getattr(product, "pattern", ""),  # Vereist for clothing
            # Vereist for clothing/toys
            "age group": "",
            "multipack": "",  # Vereist in some countries (int)
            "is bundle": "no",  # Vereist in some countries
            "unit pricing measure": unit,  # Voor regelgeving
            "unit pricing base measure": "",  # Voor regelgeving
            "energy efficiency class": "",  # Optioneel
            "min energy efficiency class": "",
            "max energy efficiency class": "",
            "item group id": "",
            "sell on google quantity": product.stock.quantity if product.stock.quantity else 0,
        }
