from django.test import TestCase
from django.contrib.sessions.middleware import SessionMiddleware
from django.test.client import RequestFactory
from ecommerce_website.classes.model.shopping_cart import ShoppingCart
from ecommerce_website.models import Product


class ShoppingCartTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = SessionMiddleware(lambda request: None)

        self.product1 = Product.objects.create(name='Product 1', price=10)
        self.product2 = Product.objects.create(name='Product 2', price=20)

    def test_add_item(self):
        request = self.factory.get('/')
        self.middleware.process_request(request)
        request.session.save()        
        
        cart = ShoppingCart(request)

        cart.add_item(self.product1.id, quantity=2)

        self.assertEqual(cart.cart_items, [
                         {'product_id': str(self.product1.id), 'quantity': 2}])

    def test_remove_item(self):
        request = self.factory.get('/')
        self.middleware.process_request(request)
        request.session.save()

        cart = ShoppingCart(request)

        cart.add_item(self.product1.id, quantity=1)

        cart.remove_item(self.product1.id)

        self.assertEqual(cart.cart_items, [])

    def test_update_quantity(self):
        request = self.factory.get('/')
        self.middleware.process_request(request)
        request.session.save()

        cart = ShoppingCart(request)

        cart.add_item(self.product1.id, quantity=1)

        cart.update_quantity(self.product1.id, quantity=3)

        self.assertEqual(cart.cart_items, [
                         {'product_id': str(self.product1.id), 'quantity': 3}])

    def test_total_price(self):
        request = self.factory.get('/')
        self.middleware.process_request(request)
        request.session.save()

        cart = ShoppingCart(request)

        cart.add_item(self.product1.id, quantity=2)
        cart.add_item(self.product2.id, quantity=1)

        total_price = cart.total_price

        self.assertEqual(total_price, 40)

    def test_clear_cart(self):
        request = self.factory.get('/')
        self.middleware.process_request(request)
        request.session.save()

        cart = ShoppingCart(request)
        cart.add_item(1, quantity=2)
        cart.add_item(2, quantity=3)

        cart.clear_cart()

        self.assertEqual(cart.cart_items, [])
