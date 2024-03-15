from abc import ABC, abstractmethod

class ProductServiceInterface(ABC):
    @abstractmethod
    def get_product_by_id(self, product_id):
        pass

    @abstractmethod
    def get_all_products(self):
        pass
