from abc import ABC, abstractmethod


class ProductCategoryServiceInterface(ABC):
    @abstractmethod
    def get_product_category_by_id(product_category_id):
        pass

    @abstractmethod
    def get_all_product_categories():
        pass

    @abstractmethod
    def get_all_active_product_categories():
        pass
