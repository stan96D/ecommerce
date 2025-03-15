from ecommerce_website.models import ProductCategory
from ecommerce_website.services.product_category_service.base_product_category_service import ProductCategoryServiceInterface
import json


class ProductCategoryService(ProductCategoryServiceInterface):
    @staticmethod
    def get_product_category_by_id(product_category_id):
        try:
            return ProductCategory.objects.get(id=product_category_id)
        except ProductCategory.DoesNotExist:
            return None

    @staticmethod
    def get_product_category_by_name(product_category_name):
        try:
            return ProductCategory.objects.filter(name=product_category_name).first()
        except ProductCategory.DoesNotExist:
            return None

    @staticmethod
    def get_all_product_categories():
        try:
            return ProductCategory.objects.all()
        except ProductCategory.DoesNotExist:
            return None

    @staticmethod
    def get_all_active_product_categories():
        try:
            return ProductCategory.objects.filter(active=True)
        except ProductCategory.DoesNotExist:
            return None

    @staticmethod
    def get_all_active_head_product_categories():
        try:
            return ProductCategory.objects.filter(active=True, for_homepage=True, parent_category=None)
        except ProductCategory.DoesNotExist:
            return None

    @staticmethod
    def get_all_active_head_product_categories_with_max():
        try:
            # Fetching all top-level product categories that are active and for homepage
            categories = ProductCategory.objects.filter(
                active=True, for_homepage=True, parent_category=None)

            # A helper function to limit subcategories to a maximum of 6, recursively
            def limit_subcategories(category):
                # Limit the direct subcategories of the current category to 6
                subcategories = category.subcategories.all()[:6]

                # Apply the same limit recursively for each subcategory
                for subcategory in subcategories:
                    limit_subcategories(subcategory)

                # Return the subcategories limited to 6
                return subcategories

            categories_data = []

            # Apply the limit_subcategories function to each top-level category
            for category in categories:
                # Limit subcategories for the current category
                limited_subcategories = limit_subcategories(category)

                # Create a dictionary for the category with limited subcategories
                category_data = {
                    'id': category.id,
                    'name': category.name,
                    'subcategories': [
                        {
                            'id': subcategory.id,
                            'name': subcategory.name,
                            'subcategories': [
                                {
                                    'id': sub_subcategory.id,
                                    'name': sub_subcategory.name
                                }
                                for sub_subcategory in subcategory.subcategories.all()[:6]
                            ]  # Only include the first 6 sub-subcategories
                        }
                        for subcategory in limited_subcategories
                    ]
                }
                categories_data.append(category_data)

            # Return the categories data as JSON
            return categories_data
        except ProductCategory.DoesNotExist:
            return None
