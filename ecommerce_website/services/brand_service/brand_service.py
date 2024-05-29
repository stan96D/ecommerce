from ecommerce_website.models import *


class BrandService():

    @staticmethod
    def get_all_brands():
        try:
            brand_attributes = ProductAttribute.objects.filter(
                attribute_type__name="Merk")

            unique_brands = brand_attributes.values_list(
                'value', flat=True).distinct()
            return unique_brands
        except ProductAttribute.DoesNotExist:
            return None
