from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

class ProductAttributeType(models.Model):
    name = models.CharField(max_length=100)


class ProductAttribute(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='attributes')
    attribute_type = models.ForeignKey(
        ProductAttributeType, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)
