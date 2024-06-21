from ecommerce_website.models import *


class BrandService():

    @staticmethod
    def get_all_brands():
        try:
            brands = Brand.objects.all()

            return brands
        except Brand.DoesNotExist:
            return None
