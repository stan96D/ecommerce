from abc import ABC, abstractmethod

class OrderServiceInterface(ABC):
    @abstractmethod
    def get_order_by_id(self, order_id):
        pass

    @abstractmethod
    def get_all_orders(self):
        pass

