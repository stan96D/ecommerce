from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.core.exceptions import ValidationError


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    thumbnail = models.ImageField(
        upload_to='product_thumbnails/', null=True, blank=True)
    images = models.ManyToManyField(
        'ProductImage', related_name='products', blank=True)
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=9.00) 
    runner = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def total_price_with_tax(self):
        total_price = self.price + (self.price * self.tax / 100)
        return total_price
    

class ProductSale(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00)
    dealname = models.CharField(max_length=100)
    begin_date = models.DateField(default=timezone.now)
    end_date = models.DateField()

    def __str__(self):
        return f"Sale for {self.product.name}: {self.dealname}"

    def save(self, *args, **kwargs):
        if not self.pk:  
            ProductSale.objects.filter(
                product=self.product, active=True).update(active=False)
        super().save(*args, **kwargs)

    def clean(self):
        if self.begin_date >= self.end_date:
            raise ValidationError("Begin date must be before end date")

        if self.active:
            existing_active_sale = ProductSale.objects.filter(
                product=self.product, active=True).first()
            if existing_active_sale and existing_active_sale != self:
                raise ValidationError(
                    "Another active sale already exists for this product")
            

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
    thumbnail = models.ImageField(
        upload_to='category_thumbnails/', null=True, blank=True)

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
    

class OrderLine(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey(
        'Order', related_name='order_lines', on_delete=models.CASCADE, default=None)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)

class Order(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    payment_information = models.TextField()
    deliver_date = models.DateField()
    deliver_method = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)
    shipping_address = models.TextField()
    billing_address = models.TextField()

    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    sub_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    tax_price_low = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    tax_price_high = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    shipping_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)




