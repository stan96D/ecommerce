from django.db.models import QuerySet


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
            sorted_queryset = sorted(queryset, key=lambda x: getattr(x, attribute))
            if order == 'descending':
                sorted_queryset.reverse()
            return sorted_queryset
        else:
            return queryset