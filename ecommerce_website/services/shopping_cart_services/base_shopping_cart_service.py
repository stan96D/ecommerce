from abc import ABC, abstractmethod


class AbstractShoppingCartService(ABC):
    @abstractmethod
    def add_item(self, product_id, quantity=1):
        pass

    @abstractmethod
    def remove_item(self, product_id):
        pass

    @abstractmethod
    def update_quantity(self, product_id, quantity):
        pass

    @abstractmethod
    def clear_cart(self):
        pass

    @property
    @abstractmethod
    def cart_items(self):
        pass

    @property
    @abstractmethod
    def total_price(self):
        pass

    @property
    @abstractmethod
    def count(self):
        pass
