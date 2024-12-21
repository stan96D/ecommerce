from django.core.cache import cache
from ecommerce_website.services.product_service.product_service import ProductService
from decimal import Decimal
from ecommerce_website.classes.model.base_shopping_cart_service import *


class SessionShoppingCart(ShoppingCartInterface):
    def __init__(self, request, shipping_price=0, discount_amount=0):
        self.session = request.session

        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

        self.shipping_price = shipping_price
        self.discount_amount = discount_amount

    def add_item(self, product_id, quantity):
        product_id = str(product_id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0}
        self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove_item(self, product_id):
        product_id = str(product_id)
        print("Delete:", product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def update_quantity(self, product_id, quantity):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
            self.save()

    def clear_cart(self):
        self.cart = self.session['cart'] = {}
        self.save()

    def save(self):
        self.session.modified = True

    @property
    def cart_items(self):
        return [
            {'product_id': product_id, 'quantity': item['quantity']}
            for product_id, item in self.cart.items()
        ]

    @property
    def get_shipping_price(self):
        return self.shipping_price

    @property
    def get_discount_amount(self):
        return self.discount_amount

    @property
    def total_price(self):
        total = 0
        for product_id, item in self.cart.items():
            product = ProductService.get_product_by_id(product_id)
            if product is not None:
                if product.has_product_sale:
                    product_price = product.unit_sale_price
                else:
                    product_price = product.unit_selling_price
                print("PRIJS", product_price)
                subtotal = item['quantity'] * product_price
                total += subtotal

        shipping_price = self.shipping_price
        discount_amount = self.discount_amount

        total -= discount_amount
        total += shipping_price
        print("SHOPPINGPRICE:", shipping_price, discount_amount, total)
        return total

    @property
    def sub_total(self):
        subtotal_amount = Decimal(0)
        for product_id, item in self.cart.items():
            product = ProductService.get_product_by_id(product_id)
            if product is not None:
                if product.has_product_sale:
                    product_price = product.unit_sale_price
                else:
                    product_price = product.unit_selling_price
                subtotal_amount += item['quantity'] * product_price

        total_tax_low = self.total_tax(9)
        total_tax_high = self.total_tax(21)

        total_tax = total_tax_low + total_tax_high

        return (subtotal_amount - total_tax).quantize(Decimal('0.00'))

    def total_tax(self, tax_percentage):
        total_tax_amount = Decimal(0)
        for product_id, item in self.cart.items():
            product = ProductService.get_product_by_id(product_id)
            if product is not None:
                # Determine the product price (sale or regular)
                product_price = (
                    product.unit_sale_price if product.has_product_sale else product.unit_selling_price
                )

                # Calculate the subtotal for the product
                subtotal = item['quantity'] * product_price

                # Calculate the tax amount based on the subtotal
                tax_amount = subtotal * \
                    (Decimal(tax_percentage) / (100 + tax_percentage))

                total_tax_amount += tax_amount

        # Return the total tax amount rounded to two decimal places
        return total_tax_amount.quantize(Decimal('0.00'))

    def to_json(self):
        cart_data = {
            'subtotal': float(self.sub_total),
            'total_price': float(self.total_price),
            'items': []
        }

        for product_id, item in self.cart.items():
            product = ProductService.get_product_by_id(product_id)

            product_type_attr = product.attributes.all().filter(
                attribute_type__name='Producttype').first()
            product_type = product_type_attr.value if product_type_attr else 'Vloer'

            product_unit_attr = product.attributes.all().filter(
                attribute_type__name='Eenheid').first()
            product_unit = product_unit_attr.value if product_unit_attr else 'm²'

            if product is not None:
                product_price = product.unit_sale_price if product.has_product_sale else product.unit_selling_price

                if product.thumbnail and product.thumbnail.url:
                    thumbnail_url = product.thumbnail.url
                else:
                    thumbnail_url = "/static/images/no_image_placeholder.png"

                item_data = {
                    'product_id': product_id,
                    'name': product.name,
                    'product_type': product_type,
                    'unit': product_unit,
                    'thumbnail': thumbnail_url,
                    'unit_sale_price': float(product.unit_sale_price) if product.has_product_sale else None,
                    'unit_price': float(product.unit_selling_price),
                    'price': float(product_price),
                    'quantity': item['quantity'],
                    'subtotal': float(item['quantity'] * product_price),
                    'totalPrice': float(item['quantity'] * product_price)
                }
                cart_data['items'].append(item_data)

        return cart_data


class AccountShoppingCart(ShoppingCartInterface):

    def __init__(self, shipping_price=0, discount_amount=0):
        self.cart = cache.get('cached_cart') or {}

        self.shipping_price = shipping_price
        self.discount_amount = discount_amount

    def add_item(self, product_id, quantity):
        product_id = str(product_id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0}
        self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove_item(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def update_quantity(self, product_id, quantity):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
            self.save()

    def clear_cart(self):
        self.cart = {}
        self.save()

    def save(self):
        cache.set('cached_cart', self.cart, timeout=3600)

    @property
    def cart_items(self):
        return [
            {'product_id': product_id, 'quantity': item['quantity']}
            for product_id, item in self.cart.items()
        ]

    @property
    def get_shipping_price(self):
        return self.shipping_price

    @property
    def get_discount_amount(self):
        return self.discount_amount

    @property
    def total_price(self):
        total = 0
        for product_id, item in self.cart.items():
            product = ProductService.get_product_by_id(product_id)
            if product is not None:
                if product.has_product_sale:
                    product_price = product.unit_sale_price
                else:
                    product_price = product.unit_selling_price
                subtotal = item['quantity'] * product_price
                total += subtotal

        shipping_price = self.shipping_price
        discount_amount = self.discount_amount

        total += shipping_price
        total -= discount_amount

        return total

    @property
    def sub_total(self):
        subtotal_amount = Decimal(0)
        for product_id, item in self.cart.items():
            product = ProductService.get_product_by_id(product_id)
            if product is not None:
                if product.has_product_sale:
                    product_price = product.unit_sale_price
                else:
                    product_price = product.unit_selling_price
                subtotal_amount += item['quantity'] * product_price

        total_tax_low = self.total_tax(9)
        total_tax_high = self.total_tax(21)

        total_tax = total_tax_low + total_tax_high

        return (subtotal_amount - total_tax).quantize(Decimal('0.00'))

    def total_tax(self, tax_percentage):
        total_tax_amount = Decimal(0)
        for product_id, item in self.cart.items():
            product = ProductService.get_product_by_id(product_id)
            if product is not None and product.tax == tax_percentage:
                if product.has_product_sale:
                    product_price = product.unit_sale_price
                else:
                    product_price = product.unit_selling_price
                subtotal = item['quantity'] * product_price
                tax_amount = subtotal * (Decimal(tax_percentage) / 100)
                total_tax_amount += tax_amount
        return total_tax_amount.quantize(Decimal('0.00'))

    def to_json(self):
        cart_data = {
            'subtotal': float(self.sub_total),
            'total_price': float(self.total_price),
            'items': []
        }

        for product_id, item in self.cart.items():
            product = ProductService.get_product_by_id(product_id)

            product_type_attr = product.attributes.all().filter(
                attribute_type__name='Producttype').first()
            product_type = product_type_attr.value if product_type_attr else 'Vloer'

            product_unit_attr = product.attributes.all().filter(
                attribute_type__name='Eenheid').first()
            product_unit = product_unit_attr.value if product_unit_attr else 'm²'

            if product is not None:
                product_price = product.unit_sale_price if product.has_product_sale else product.unit_selling_price

                if product.thumbnail and product.thumbnail.url:
                    thumbnail_url = product.thumbnail.url
                else:
                    thumbnail_url = "/static/images/no_image_placeholder.png"

                item_data = {
                    'product_id': product_id,
                    'name': product.name,
                    'product_type': product_type,
                    'unit': product_unit,
                    'thumbnail': thumbnail_url,
                    'unit_sale_price': float(product.unit_sale_price) if product.has_product_sale else None,
                    'unit_price': float(product.unit_selling_price),
                    'price': float(product_price),
                    'quantity': item['quantity'],
                    'subtotal': float(item['quantity'] * product_price),
                    'totalPrice': float(item['quantity'] * product_price)
                }
                cart_data['items'].append(item_data)

        return cart_data
