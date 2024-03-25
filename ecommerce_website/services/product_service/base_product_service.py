from abc import ABC, abstractmethod

class ProductServiceInterface(ABC):
    @abstractmethod
    def get_product_by_id(self, product_id):
        pass

    @abstractmethod
    def get_all_products(self):
        pass

    @abstractmethod
    def get_products_by_attribute(attribute):
        pass

    @abstractmethod
    def get_all_products_by_id(self, product_ids):
        pass

    @abstractmethod
    def get_products_by_search(search_string):
        pass

    @abstractmethod
    def get_products_by_attributes_and_values(attributes, category):
        pass
