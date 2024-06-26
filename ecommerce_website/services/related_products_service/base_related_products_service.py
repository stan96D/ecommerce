from abc import ABC, abstractmethod


class RelatedProductInterface():
    @abstractmethod
    def get_related_by_product(product_id):
        pass


