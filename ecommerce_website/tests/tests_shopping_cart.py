from django.test import TestCase
from django.contrib.sessions.middleware import SessionMiddleware
from django.test.client import RequestFactory
from ecommerce_website.classes.model.shopping_cart import SessionShoppingCart
from ecommerce_website.models import Product
from decimal import Decimal

class ShoppingCartTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = SessionMiddleware(lambda request: None)

        self.product1 = Product.objects.create(
            name='Product 1', unit_price=10, tax=9.00)
        self.product2 = Product.objects.create(name='Product 2', unit_price=20, tax=21.00)

    def test_add_item(self):
        request = self.factory.get('/')
        self.middleware.process_request(request)
        request.session.save()        
        
        cart = SessionShoppingCart(request)

        cart.add_item(self.product1.id, quantity=2)

        self.assertEqual(cart.cart_items, [
                         {'product_id': str(self.product1.id), 'quantity': 2}])

    def test_remove_item(self):
        request = self.factory.get('/')
        self.middleware.process_request(request)
        request.session.save()

        cart = SessionShoppingCart(request)

        cart.add_item(self.product1.id, quantity=1)

        cart.remove_item(self.product1.id)

        self.assertEqual(cart.cart_items, [])

    def test_add_duplicate_items(self):
        request = self.factory.get('/')
        self.middleware.process_request(request)
        request.session.save()

        cart = SessionShoppingCart(request)

        cart.add_item(self.product1.id, quantity=1)
        cart.add_item(self.product1.id, quantity=1)
        cart.add_item(self.product1.id, quantity=1)

        self.assertEqual(cart.cart_items, [
                         {'product_id': str(self.product1.id), 'quantity': 3}])
        

    def test_update_quantity(self):
        request = self.factory.get('/')
        self.middleware.process_request(request)
        request.session.save()

        cart = SessionShoppingCart(request)

        cart.add_item(self.product1.id, quantity=1)

        cart.update_quantity(self.product1.id, quantity=3)

        self.assertEqual(cart.cart_items, [
                         {'product_id': str(self.product1.id), 'quantity': 3}])

    def test_total_price(self):
        request = self.factory.get('/')
        self.middleware.process_request(request)
        request.session.save()

        cart = SessionShoppingCart(request)

        cart.add_item(self.product1.id, quantity=2)
        cart.add_item(self.product2.id, quantity=1)

        total_price = cart.total_price

        self.assertEqual(total_price, 40)

    def test_total_price_discount(self):
        request = self.factory.get('/')
        self.middleware.process_request(request)
        request.session.save()

        cart = SessionShoppingCart(request, discount_amount=25)

        cart.add_item(self.product1.id, quantity=2)
        cart.add_item(self.product2.id, quantity=1)

        total_price = cart.total_price

        self.assertEqual(total_price, 15)

    def test_total_price_shipping_cost(self):
        request = self.factory.get('/')
        self.middleware.process_request(request)
        request.session.save()

        cart = SessionShoppingCart(request, shipping_price=5)

        cart.add_item(self.product1.id, quantity=2)
        cart.add_item(self.product2.id, quantity=1)

        total_price = cart.total_price

        self.assertEqual(total_price, 45)

    def test_total_price_shipping_cost_and_discount(self):
        request = self.factory.get('/')
        self.middleware.process_request(request)
        request.session.save()

        cart = SessionShoppingCart(request, shipping_price=5, discount_amount=10)

        cart.add_item(self.product1.id, quantity=2)
        cart.add_item(self.product2.id, quantity=1)

        total_price = cart.total_price

        self.assertEqual(total_price, 35)

    def test_tax_low(self):
        request = self.factory.get('/')
        self.middleware.process_request(request)
        request.session.save()

        cart = SessionShoppingCart(request)

        cart.add_item(self.product1.id, quantity=2)

        tax_low = cart.total_tax(9)

        self.assertEqual(tax_low, Decimal('1.65'))

    def test_tax_high(self):
        request = self.factory.get('/')
        self.middleware.process_request(request)
        request.session.save()

        cart = SessionShoppingCart(request)

        cart.add_item(self.product2.id, quantity=1)

        tax_high = cart.total_tax(21)

        self.assertEqual(tax_high, Decimal('3.47'))

    def test_clear_cart(self):
        request = self.factory.get('/')
        self.middleware.process_request(request)
        request.session.save()

        cart = SessionShoppingCart(request)
        cart.add_item(self.product1.id, quantity=2)
        cart.add_item(self.product2.id, quantity=1)

        cart.clear_cart()

        self.assertEqual(cart.cart_items, [])
