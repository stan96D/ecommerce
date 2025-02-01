from ecommerce_website.models import Product
from ecommerce_website.services.export_service.base_export_service import BaseExportService


class ProductExportService(BaseExportService):
    def __init__(self, queryset=None):
        queryset = queryset or Product.objects.all()
        super().__init__(queryset)

    def process_record(self, product):
        """
        Process each individual product and extract the necessary data.
        """

        product_data = {
            "Artikelnummer (sku)": product.sku,
            "Productnaam (name)": product.name,
            "Leverancier (supplier)": product.supplier,
            # Convert Decimal to float
            "Inkoopprijs excl btw per doos (unit_price)": float(product.unit_price),
            # Convert Decimal to float
            "Inkoopprijs excl btw per m² (price)": float(product.price),
            "Afbeelding (thumbnail)": product.thumbnail_url,
            # Convert Decimal to float
            "BTW (tax)": float(product.tax),
            "Hardloper (runner)": product.runner,
            # Convert Decimal to float
            "Verkoopmarge (selling_percentage)": float(product.selling_percentage),
            # Convert Decimal to float
            "Verkoopprijs incl btw per doos (unit_selling_price)": float(product.unit_selling_price),
            # Convert Decimal to float
            "Verkoopprijs incl btw per m² (selling_price)": float(product.selling_price),
            # Convert Decimal to float
            "Kortingsprijs incl btw per m² (sale_price)": float(product.sale_price) if product.sale_price else None,
            # Convert Decimal to float
            "Kortingsprijs incl btw per doos (unit_sale_price)": float(product.unit_sale_price) if product.unit_sale_price else None,
            "Korting? (has_product_sale)": product.has_product_sale,
            "Voorraad (stock)": product.stock.quantity,
        }
        return product_data
