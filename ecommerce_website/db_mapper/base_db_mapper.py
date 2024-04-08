from abc import ABC, abstractmethod

class DatabaseMapperInterface(ABC):

    @abstractmethod
    def map_products(self, product_json):
        pass
