from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Product)
admin.site.register(ProductAttribute)
admin.site.register(ProductAttributeType)
admin.site.register(ProductStock)
admin.site.register(ProductImage)
admin.site.register(ProductCategory)
admin.site.register(ProductCategoryAttribute)



