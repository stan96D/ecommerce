from django.db import models
from django.utils.text import slugify


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    thumbnail = models.ImageField(
        upload_to='product_thumbnails/', null=True, blank=True)
    images = models.ManyToManyField('ProductImage', related_name='products')


    def __str__(self):
        return self.name


class ProductAttributeType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, default=None, null=True)
    parent_category = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    active = models.BooleanField(default=True)


    def __str__(self):
        if self.parent_category:
            return f"{self.parent_category.name} - {self.name}"
        else:
            return self.name

    
class ProductAttribute(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='attributes')
    attribute_type = models.ForeignKey(
        ProductAttributeType, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.product.name} - {self.attribute_type.name} - {self.value}"

class ProductStock(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name='stock')
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - Quantity: {self.quantity}"


class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_images/')


class ProductFilter(models.Model):
    name = models.CharField(max_length=100)
    product_attributes = models.ManyToManyField(ProductAttribute)
    parent_category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} (Category: {self.parent_category.name})"










