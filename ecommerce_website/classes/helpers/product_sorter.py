

class ProductSorter:
    SORT_OPTIONS = {
        'Prijs oplopend': {'attribute': 'price', 'order': 'ascending'},
        'Prijs aflopend': {'attribute': 'price', 'order': 'descending'},
    }

    @classmethod
    def sort_products_by(cls, queryset, sort_option: str) -> list:
        sort_data = cls.SORT_OPTIONS.get(sort_option)
        if sort_data:
            attribute = sort_data['attribute']
            order = sort_data['order']
            sorted_queryset = sorted(
                queryset, key=lambda x: getattr(x, attribute))
            if order == 'descending':
                sorted_queryset.reverse()
            return sorted_queryset
        else:
            return queryset


class ProductSorterUtility:

    @staticmethod
    def is_paginated(attributes):
        return 'page' in attributes

    @staticmethod
    def is_sort(attributes):
        return 'tn_sort' in attributes

    @staticmethod
    def is_filter(attributes):
        return 'tn_sort' not in attributes and len(
            attributes) > 0 or 'tn_sort' in attributes and len(
            attributes) > 1

    @staticmethod
    def is_search_filter(attributes):
        return ('tn_sort' not in attributes and 'q' not in attributes and len(attributes) > 0) or ('tn_sort' in attributes and 'q' not in attributes and len(attributes) > 1) or (
            'tn_sort' not in attributes and 'q' in attributes and len(attributes) > 1) or ('tn_sort' in attributes and 'q' in attributes and len(attributes) > 2)
