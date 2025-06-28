from decimal import InvalidOperation
from django.contrib import admin

# Register your models here.
from .models import *

from django.contrib import admin
from .models import Product
from django.contrib import admin
from .models import Product, ProductSale, Sale
from django.contrib import admin
from .models import Sale, ProductSale


from decimal import InvalidOperation


class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name', 'sku']
    list_display = ['name', 'sku']
    exclude = ['thumbnail_url']
    readonly_fields = [
        'unit_selling_price_excl_tax',
        'selling_price_excl_tax',
        'unit_selling_price',
        'selling_price',
    ]

    def unit_selling_price_excl_tax(self, obj):
        try:
            return round(obj.unit_selling_price_excl_tax, 2)
        except (AttributeError, InvalidOperation):
            return "-"
    unit_selling_price_excl_tax.short_description = 'Unit Selling Price Excl. Tax'

    def selling_price_excl_tax(self, obj):
        try:
            return round(obj.selling_price_excl_tax, 2)
        except (AttributeError, InvalidOperation):
            return "-"
    selling_price_excl_tax.short_description = 'Selling Price Excl. Tax'

    def unit_selling_price(self, obj):
        try:
            return round(obj.unit_selling_price, 2)
        except (AttributeError, InvalidOperation):
            return "-"
    unit_selling_price.short_description = 'Unit Selling Price (Incl. Tax)'

    def selling_price(self, obj):
        try:
            return round(obj.selling_price, 2)
        except (AttributeError, InvalidOperation):
            return "-"
    selling_price.short_description = 'Selling Price (Incl. Tax)'


# Register the Sale admin
admin.site.register(Sale)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductAttribute)
admin.site.register(ProductAttributeType)
admin.site.register(ProductStock)
admin.site.register(ProductImage)
admin.site.register(ProductCategory)
admin.site.register(ProductFilter)
admin.site.register(Order)
admin.site.register(OrderLine)
admin.site.register(ProductSale)
admin.site.register(DeliveryMethod)
admin.site.register(Account)
admin.site.register(StoreMotivation)
admin.site.register(Brand)
admin.site.register(Store)
admin.site.register(ReturnOrder)
admin.site.register(ReturnOrderLine)
admin.site.register(StoreRating)
