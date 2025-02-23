import uuid
from decimal import Decimal
from django.utils.timezone import now
from datetime import date
from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AnonymousUser
from ecommerce_website.settings.webshop_config import WebShopConfig
from django.db.models import Sum


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
    phone_number = models.CharField(max_length=20)
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
    DELIVERY_TYPE_CHOICES = [
        ('delivery', 'Delivery'),
        ('takeaway', 'Takeaway'),
    ]

    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    delivery_days = models.DecimalField(
        max_digits=2, decimal_places=0, default=9)
    active = models.BooleanField(default=True)
    delivery_type = models.CharField(
        max_length=10, choices=DELIVERY_TYPE_CHOICES, default='delivery'
    )
    additional_info = models.CharField(max_length=100, null=True, blank=True)


class Product(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    supplier = models.CharField(
        max_length=100, db_index=True, default='Unknown')
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, db_index=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, db_index=True)
    thumbnail_url = models.URLField(
        max_length=500, blank=True, null=True)
    tax = models.DecimalField(
        max_digits=5, decimal_places=2, default=21, db_index=True)
    runner = models.BooleanField(default=False)
    selling_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00)
    sku = models.CharField(
        max_length=50, unique=True, db_index=True)

    @property
    def buy_price_excl_tax(self):
        tax_multiplier = Decimal("1.00") + (self.tax / Decimal('100'))
        return round(self.price / tax_multiplier, 2)

    @property
    def unit_buy_price_excl_tax(self):
        tax_multiplier = Decimal("1.00") + (self.tax / Decimal('100'))
        return round(self.unit_price / tax_multiplier, 2)

    @property
    def unit_selling_price(self):

        excl_tax = self.unit_price

        selling_price_excl_tax = round(
            excl_tax * self.selling_percentage, 2)

        selling_price_excl_tax_shipping = selling_price_excl_tax * \
            WebShopConfig.shipping_margin()

        tax_multiplier = Decimal("1.00") + (self.tax / Decimal('100'))

        selling_price_incl_tax = round(
            selling_price_excl_tax_shipping * tax_multiplier, 2)

        return selling_price_incl_tax

    @property
    def selling_price(self):

        excl_tax = self.price

        selling_price_excl_tax = round(
            excl_tax * self.selling_percentage, 2)

        selling_price_excl_tax_shipping = selling_price_excl_tax * \
            WebShopConfig.shipping_margin()

        tax_multiplier = Decimal("1.00") + (self.tax / Decimal('100'))

        selling_price_incl_tax = round(
            selling_price_excl_tax_shipping * tax_multiplier, 2)

        return selling_price_incl_tax

    def __str__(self):
        return self.sku + ": " + self.name

    @property
    def search_string(self):
        attribute_values = self.attributes.exclude(
            attribute_type__name='Omschrijving').values_list('value', flat=True)
        attribute_string = ' '.join(attribute_values)
        return f"{self.name} {attribute_string}"

    @property
    def has_product_sale(self):
        # Only one sale can be used
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
    description = models.CharField(max_length=100)

    begin_date = models.DateField(default=now)
    end_date = models.DateField()

    def __str__(self):
        return self.name

    @property
    def days_left(self):
        """Calculate the number of days left until the sale ends."""
        today = date.today()
        if self.end_date >= today:
            return (self.end_date - today).days
        return 0  # Return 0 if the sale has ended


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

    numeric_value = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        db_index=True,
        null=True,
        blank=True,
        default=None
    )

    additional_data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.attribute_type.name} - {self.value}"


class ProductStock(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name='stock')
    quantity = models.IntegerField(default=0)
    delivery_date = models.DateField(
        null=True, blank=True)  # Nullable delivery date

    def __str__(self):
        return f"{self.product}: {self.product.name} - Quantity: {self.quantity}"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images', default=False)
    image_url = models.URLField(
        max_length=500, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.product.name}"


class Brand(models.Model):
    name = models.CharField(unique=True, max_length=100)
    image = models.ImageField(
        upload_to='brand_images/', null=True, blank=True)


class ProductFilter(models.Model):
    TYPE_CHOICES = [
        ('option', 'Option'),
        ('slider', 'Slider'),
    ]

    name = models.CharField(max_length=100)
    filter_type = models.CharField(
        max_length=10, choices=TYPE_CHOICES, default='option')
    values = models.JSONField()
    unit_value = models.CharField(
        max_length=10, default=None,
        null=True,
        blank=True)
    parent_category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE, null=True)

    class Meta:
        # Ensures unique name per category
        unique_together = ('name', 'parent_category')

    def __str__(self):
        if self.parent_category:
            return f"{self.filter_type} {self.name} (Category: {self.parent_category.name})"
        else:
            return f"{self.filter_type} {self.name}"


class StoreMotivation(models.Model):
    name = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=False)
    text = models.CharField(max_length=200, null=True)
    icon = models.CharField(max_length=20, null=True, blank=True)
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

    delivery_date = models.DateField(
        null=True, blank=True)
    count_delivered = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        if self.order.account:
            return f'OrderLine {self.id} for account with name {self.order.account.first_name} {self.order.account.last_name} and product {self.product.name}'
        else:
            return f'OrderLine {self.id} with no associated account and product {self.product.name}'

    def has_return_order(self):
        """Returns True if this OrderLine has an associated ReturnOrder."""
        return self.return_order is not None

    def accumulated_return_quantity(self):
        """Returns the accumulated quantity of related ReturnOrderLines."""
        return self.return_order_lines.aggregate(
            total_quantity=Sum('quantity')
        )['total_quantity'] or 0  # If no return order lines, return 0


class Order(models.Model):

    ORDER_STATUS_CHOICES = [
        ('open', 'Openstaand'),
        ('paid', 'Betaald'),
        ('delivered', 'Geleverd'),
        ('partly', 'Deels geleverd'),
        ('failed', 'Mislukt'),

    ]

    salutation = models.CharField(max_length=100, default="Geen van beiden")
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
        default='open', choices=ORDER_STATUS_CHOICES)

    # Token for secure access
    token = models.CharField(max_length=64, unique=True, blank=True)

    def save(self, *args, **kwargs):
        # Generate a token if it doesn't already exist
        if not self.token:
            self.token = uuid.uuid4().hex  # Generate a unique 32-character token
        super().save(*args, **kwargs)

    @property
    def is_paid(self):
        return self.order_status == 'paid' and self.payment_status == 'paid'

    @property
    def can_be_returned(self):
        return timezone.now() <= self.created_date + timedelta(days=WebShopConfig.return_days())

    def __str__(self):
        if self.account:
            return f'Order {self.id} for account with name {self.account.first_name} {self.account.last_name}'
        else:
            return f'Order {self.id} with no associated account'


class ReturnOrder(models.Model):
    RETURN_STATUS_CHOICES = [
        ('open', 'Openstaand'),
        ('paid', 'Betaald'),
        ('delivered', 'Opgehaald'),
        ('partly', 'Deels opgehaald'),
        ('failed', 'Mislukt'),
        ('done', 'Afgerond'),

    ]

    order = models.ForeignKey(
        Order, related_name='returns', on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.CharField(
        max_length=20, choices=RETURN_STATUS_CHOICES, default='open')
    created_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    refund_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    shipping_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    sub_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    tax_price_low = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    tax_price_high = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)

    # User-related fields
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_address = models.EmailField()
    phone = models.CharField(max_length=20)

    shipping_address = models.TextField()
    billing_address = models.TextField()

    payment_information = models.TextField()
    payment_information_id = models.TextField(max_length=20)
    payment_issuer = models.TextField(null=True, max_length=20)

    payment_id = models.CharField(max_length=100, unique=True, null=True)
    payment_status = models.TextField(null=True)
    payment_url = models.CharField(max_length=100, unique=True, null=True)

    deliver_date = models.DateField()
    deliver_method = models.CharField(max_length=100)
    # Token for secure access
    token = models.CharField(max_length=64, unique=True, blank=True)

    def save(self, *args, **kwargs):
        # Generate a token if it doesn't already exist
        if not self.token:
            self.token = uuid.uuid4().hex  # Generate a unique 32-character token
        super().save(*args, **kwargs)

    @property
    def is_paid(self):
        return self.status == 'paid' and self.payment_status == 'paid'

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

    delivery_date = models.DateField(
        null=True, blank=True)
    count_delivered = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f'ReturnOrderLine {self.id} for ReturnOrder {self.return_order.id}'


class Store(models.Model):
    name = models.CharField(max_length=30)
    contact_email = models.EmailField(max_length=254)
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    vat_number = models.CharField(max_length=20)
    coc_number = models.CharField(max_length=20)
    opening_time_week = models.CharField(max_length=100)
    opening_time_weekend = models.CharField(max_length=100)
    active = models.BooleanField(default=False)
    socials = models.JSONField(default=dict, blank=True)
    faq = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Store ID: {self.id}, Email: {self.contact_email}, Active: {self.active}"


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
