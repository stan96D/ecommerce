from abc import ABC, abstractmethod


class ProductCategoryAttributeServiceInterface(ABC):
    @abstractmethod
    def get_product_category_attribute_by_id(product_category_id):
        pass


    @abstractmethod
    def get_all_product_category_attributes():
        pass


    @abstractmethod
    def get_all_active_product_category_attributes():
        pass
