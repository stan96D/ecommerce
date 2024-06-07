from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from ecommerce_website.settings.webshop_config import WebShopConfig
from ecommerce_website.models import Order, OrderLine, Product
from ecommerce_website.classes.model.order_info import OrderInfo
from ecommerce_website.classes.model.address_info import AddressInfo
from ecommerce_website.classes.model.contact_info import ContactInfo
from ecommerce_website.classes.model.delivery_info import DeliveryInfo
from ecommerce_website.classes.model.payment_info import PaymentInfo
from ecommerce_website.classes.managers.order_number_manager import OrderNumberManager
from ecommerce_website.services.checkout_service.checkout_service import CheckoutService
from ecommerce_website.classes.model.shopping_cart import SessionShoppingCart
from ecommerce_website.tests.session_to_request import add_session_to_request


class CheckoutServiceTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request1 = self.factory.get('/')
        add_session_to_request(self.request1)

        self.user = AnonymousUser()

        self.product1 = Product.objects.create(
            name='Product 1', unit_price=10)
        self.product2 = Product.objects.create(
            name='Product 2', unit_price=20)

        self.shopping_cart = SessionShoppingCart(self.request1)
        self.shopping_cart.add_item(product_id=self.product1.id, quantity=2)
        self.shopping_cart.add_item(product_id=self.product2.id, quantity=1)

        self.contact_info = ContactInfo(
            first_name='John', last_name='Doe', email='john@example.com', phonenumber='123456789')
        self.billing_address_info = AddressInfo(
            address='Main St', house_number='123', city='Anytown', postal_code='12345', country='US')
        self.delivery_address_info = AddressInfo(
            address='Elm St', house_number='456', city='Othertown', postal_code='54321', country='UK')
        self.order_info = OrderInfo(self.request1)
        self.order_info.create_order(
            contact_info=self.contact_info, billing_address_info=self.billing_address_info, delivery_address_info=self.delivery_address_info)

        self.payment_info = PaymentInfo(
            payment_method='Credit Card', bank=None)

        self.delivery_info = DeliveryInfo(
            delivery_method='Standard', delivery_date='30-06-2024')

    def test_create_order(self):
        checkout_service = CheckoutService()

        initial_order_count = Order.objects.count()

        order = checkout_service.create_order(
            account=self. user,
            order_info=self.order_info,
            payment_info=self.payment_info,
            delivery_info=self.delivery_info,
            shopping_cart=self.shopping_cart
        )

        final_order_count = Order.objects.count()

        self.assertIsNotNone(order)
        self.assertEqual(final_order_count, initial_order_count + 1)

        self.assertEqual(order.order_lines.count(), 2)

        self.assertEqual(order.account, None)
        self.assertEqual(order.first_name, self.contact_info.first_name)
        self.assertEqual(order.last_name, self.contact_info.last_name)
        self.assertEqual(order.email, self.contact_info.email)
        self.assertEqual(order.phone, self.contact_info.phonenumber)
        self.assertEqual(order.payment_information,
                         self.payment_info.payment_information)
        self.assertEqual(order.deliver_date, self.delivery_info.delivery_date)
        self.assertEqual(order.deliver_method,
                         self.delivery_info.delivery_method)
        self.assertEqual(order.shipping_address,
                         self.delivery_address_info.full_address)
        self.assertEqual(order.billing_address,
                         self.billing_address_info.full_address)


        order_lines = order.order_lines.all()
        self.assertEqual(order_lines[0].product, self.product1)
        self.assertEqual(order_lines[0].quantity, 2)
        self.assertEqual(order_lines[0].unit_price,
                         10 * WebShopConfig.shipping_margin())
        self.assertEqual(order_lines[0].total_price,
                         20 * WebShopConfig.shipping_margin())
        self.assertEqual(order_lines[1].product, self.product2)
        self.assertEqual(order_lines[1].quantity, 1)
        self.assertEqual(order_lines[1].unit_price,
                         20 * WebShopConfig.shipping_margin())
        self.assertEqual(order_lines[1].total_price,
                         20 * WebShopConfig.shipping_margin())
