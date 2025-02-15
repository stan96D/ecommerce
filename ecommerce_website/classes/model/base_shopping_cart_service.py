from abc import ABC, abstractmethod


class ShoppingCartInterface(ABC):
    @abstractmethod
    def add_item(self, product_id, quantity):
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

    @abstractmethod
    def quantity_in_cart(self, product_id):
        pass

    @abstractmethod
    def to_json(self):
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
    def shipping_price(self):
        pass
