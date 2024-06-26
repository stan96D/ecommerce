from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Product)
admin.site.register(ProductAttribute)
admin.site.register(ProductAttributeType)
admin.site.register(ProductStock)
admin.site.register(ProductImage)
admin.site.register(ProductCategory)
admin.site.register(ProductFilter)
admin.site.register(Order)
admin.site.register(OrderLine)
admin.site.register(ProductSale)
admin.site.register(Sale)
admin.site.register(DeliveryMethod)
admin.site.register(Account)
admin.site.register(StoreMotivation)
admin.site.register(Brand)
admin.site.register(Store)
admin.site.register(ReturnOrder)
admin.site.register(ReturnOrderLine)
admin.site.register(RelatedProduct)
