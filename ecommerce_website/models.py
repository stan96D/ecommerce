from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AnonymousUser
from ecommerce_website.settings.webshop_config import WebShopConfig


class AccountManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    salutation = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    house_number = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'salutation',
                       'postal_code', 'address', 'house_number', 'country', 'city']

    def __str__(self):
        return self.email

    def has_perm(self, perm: str, obj: models.Model | AnonymousUser | None = ...) -> bool:
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin


class DeliveryMethod(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    delivery_days = models.DecimalField(
        max_digits=2, decimal_places=0, default=9)
    active = models.BooleanField(default=True)


class Product(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    supplier = models.CharField(
        max_length=100, db_index=True, default='Unknown')
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, db_index=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, db_index=True)
    thumbnail = models.ImageField(
        upload_to='product_thumbnails/', null=True, blank=True)
    tax = models.DecimalField(
        max_digits=5, decimal_places=2, default=9.00, db_index=True)
    runner = models.BooleanField(default=False)
    selling_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00)

    @property
    def unit_selling_price(self):
        selling_price = round(
            self.unit_price * (1 - self.selling_percentage / 100), 2)
        selling_price_with_shipping_costs = round(
            selling_price * WebShopConfig.shipping_margin(), 2)
        return selling_price_with_shipping_costs

    @property
    def selling_price(self):

        selling_price = round(
            self.price * (1 - self.selling_percentage / 100), 2)

        selling_price_with_shipping_costs = round(
            selling_price * WebShopConfig.shipping_margin(), 2)
        return selling_price_with_shipping_costs

    def __str__(self):
        return self.name

    @property
    def search_string(self):
        attribute_values = self.attributes.exclude(
            attribute_type__name='Omschrijving').values_list('value', flat=True)
        attribute_string = ' '.join(attribute_values)
        return f"{self.name} {attribute_string}"

    @property
    def has_product_sale(self):
        return self.productsale_set.filter(sale__active=True).exists()

    @property
    def sale_price(self):
        active_product_sale = self.productsale_set.filter(
            sale__active=True).first()
        if active_product_sale:
            selling_price = self.selling_price
            discount_percentage = active_product_sale.percentage
            sale_price = selling_price - \
                (selling_price * discount_percentage / 100)
            return round(sale_price, 2)
        return None

    @property
    def unit_sale_price(self):
        active_product_sale = self.productsale_set.filter(
            sale__active=True).first()
        if active_product_sale:
            selling_price = self.unit_selling_price
            discount_percentage = active_product_sale.percentage
            sale_price = selling_price - \
                (selling_price * discount_percentage / 100)
            return round(sale_price, 2)
        return None


class Sale(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=False)

    begin_date = models.DateField(default=timezone.now)
    end_date = models.DateField()

    def __str__(self):
        return self.name


class ProductSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Sale for {self.product.name} in {self.sale.name} with {self.percentage}% off"

    def save(self, *args, **kwargs):
        if self.sale.active:
            ProductSale.objects.filter(sale=self.sale, product=self.product).exclude(
                pk=self.pk)
        super().save(*args, **kwargs)

    def clean(self):
        if self.sale.begin_date >= self.sale.end_date:
            raise ValidationError("Begin date must be before end date")


class ProductAttributeType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, default=None, null=True)
    parent_category = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    active = models.BooleanField(default=True)
    for_homepage = models.BooleanField(default=True)

    thumbnail = models.ImageField(
        upload_to='category_thumbnails/', null=True, blank=True)

    def __str__(self):
        if self.parent_category:
            return f"{self.parent_category.name} - {self.name}"
        else:
            return self.name


class ProductAttribute(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='attributes', db_index=True)
    attribute_type = models.ForeignKey(
        ProductAttributeType, on_delete=models.CASCADE, db_index=True)
    value = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return f"{self.product.name} - {self.attribute_type.name} - {self.value}"


class ProductStock(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name='stock')
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - Quantity: {self.quantity}"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images', default=False)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image for {self.product.name}"


class Brand(models.Model):
    name = models.CharField(unique=True, max_length=100)
    image = models.ImageField(
        upload_to='brand_images/', null=True, blank=True)


class ProductFilter(models.Model):
    name = models.CharField(max_length=100)
    product_attributes = models.ManyToManyField(ProductAttribute)
    parent_category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE, null=True)

    def __str__(self):
        if self.parent_category:
            return f"{self.name} (Category: {self.parent_category.name})"

        else:

            return f"{self.name}"


class StoreMotivation(models.Model):
    name = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=False)
    text = models.CharField(max_length=200, null=True)
    for_homepage = models.BooleanField(default=True)
    image = models.ImageField(
        upload_to='store_motivation_images/', null=True, blank=True)


class OrderLine(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey(
        'Order', related_name='order_lines', on_delete=models.CASCADE, default=None)
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    return_order = models.ForeignKey(
        'ReturnOrder', related_name='order_lines', on_delete=models.SET_NULL, null=True, blank=True)


class Order(models.Model):

    ORDER_STATUS_CHOICES = [
        ('open', 'Openstaand'),
        ('paid', 'Betaald'),
        ('delivered', 'Geleverd'),
        ('failed', 'Mislukt'),

    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    payment_information = models.TextField()
    payment_information_id = models.TextField(default=None, max_length=20)
    payment_issuer = models.TextField(null=True, max_length=20)

    deliver_date = models.DateField()
    deliver_method = models.CharField(max_length=100)

    shipping_address = models.TextField()
    billing_address = models.TextField()
    order_number = models.CharField(max_length=20, unique=True)

    account = models.ForeignKey(
        Account, related_name='orders', on_delete=models.CASCADE, default=None, null=True)

    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    sub_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    tax_price_low = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    tax_price_high = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    shipping_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    created_date = models.DateTimeField(default=timezone.now)

    payment_id = models.CharField(max_length=100, unique=True, null=True)
    payment_status = models.TextField(null=True)
    payment_url = models.CharField(max_length=100, unique=True, null=True)

    order_status = models.TextField(
        default='Openstaand', choices=ORDER_STATUS_CHOICES)

    @property
    def is_paid(self):
        return self.order_status == 'Betaald' and self.payment_status == 'paid'

    @property
    def can_be_returned(self):
        return timezone.now() <= self.created_date + timedelta(days=WebShopConfig.return_days())


class ReturnOrder(models.Model):
    RETURN_STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('processed', 'Processed'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),

    ]

    order = models.ForeignKey(
        Order, related_name='returns', on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.CharField(
        max_length=20, choices=RETURN_STATUS_CHOICES, default='requested')
    return_date = models.DateTimeField(auto_now_add=True)
    refund_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    shipping_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'Return {self.id} for Order {self.order.id}'


class ReturnOrderLine(models.Model):
    return_order = models.ForeignKey(
        ReturnOrder, related_name='return_order_lines', on_delete=models.CASCADE)
    order_line = models.ForeignKey(
        OrderLine, related_name='return_order_lines', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    refund_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'ReturnOrderLine {self.id} for ReturnOrder {self.return_order.id}'


class Store(models.Model):
    contact_email = models.EmailField(max_length=254)
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    vat_number = models.CharField(max_length=20)
    coc_number = models.CharField(max_length=20)
    opening_time_week = models.CharField(max_length=100)
    opening_time_weekend = models.CharField(max_length=100)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.address + self.postal_code


class StoreRating(models.Model):
    user = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='store_ratings', null=True, blank=True)
    stars = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(6)], default=0)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Review - {self.stars} door {self.user if self.user else "Anonieme gebruiker"}'
