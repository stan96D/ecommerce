from abc import ABC, abstractmethod

class ProductStockServiceInterface(ABC):
    @abstractmethod
    def get_stock_by_product_id(self, product_id):
        pass

    @abstractmethod
    def get_all_stocks_by_id(self, product_ids):
        pass
