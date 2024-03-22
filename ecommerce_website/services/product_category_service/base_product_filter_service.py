from abc import ABC, abstractmethod


class ProductFilterServiceInterface():
    @abstractmethod
    def get_product_filter_by_id(product_filter_name):
        pass

    @abstractmethod
    def get_product_filters_by_category_id(product_category_id):
        pass

    @abstractmethod
    def get_product_filters_by_category_name(product_category_name):
        pass

    @abstractmethod
    def get_product_filter_by_name(product_filter_name):
        pass

    @abstractmethod
    def get_all_product_filters():
        pass
