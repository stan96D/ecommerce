from django.test import TestCase
from django.contrib.sessions.middleware import SessionMiddleware
from django.test.client import RequestFactory
from ecommerce_website.classes.model.shopping_cart import SessionShoppingCart
from ecommerce_website.models import *
from django.contrib.auth.models import User
from ecommerce_website.services.return_service.return_service import *
from ecommerce_website.classes.managers.payment_manager.mollie_client import MollieClient
from ecommerce_website.classes.managers.payment_manager.mock_payment_client import MockPaymentClient

from ecommerce_website.services.order_service.order_service import OrderService


class ReturnOrderTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        account = Account.objects.create()

        product1 = Product.objects.create(name='Product 1')
        product2 = Product.objects.create(name='Product 2')

        order = Order.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='1234567890',
            payment_information='Credit Card',
            deliver_date='2024-06-15',
            deliver_method='Standard Shipping',
            shipping_address='123 Main St, Anytown, USA',
            billing_address='123 Main St, Anytown, USA',
            order_number='TESTORDER',
            account=account,
            total_price=100.00,
            sub_price=85.00,
            tax_price_low=5.00,
            tax_price_high=10.00,
            shipping_price=10.00,
            payment_id='2oxsqDdMPTXFMdzJWBxE9')

        OrderLine.objects.create(
            product=product1,
            quantity=2,
            order=order,
            unit_price=25.00,
            total_price=50.00
        )

        OrderLine.objects.create(
            product=product2,
            quantity=1,
            order=order,
            unit_price=35.00,
            total_price=35.00
        )

        cls.order = order

    def test_get_payment(self):

        payment_client = MockPaymentClient()

        order = self.order

        payment = payment_client.create_payment('EUR', '400.00', order.order_number,
                                                     'redirect.example', 'webhook.example', 'ideal', 'ideal_SNSBNL2A')
        
        found_payment = payment_client.get_payment(payment['id'])

        self.assertEqual(found_payment['id'], payment['id'])


    def test_refund_order(self):

        payment_client = MockPaymentClient()
        service = ReturnService(payment_client)

        order = self.order

        payment = payment_client.create_payment('EUR', '400.00', order.order_number,
                                                     'redirect.example', 'webhook.example', 'ideal', 'ideal_SNSBNL2A')

        OrderService.add_payment(payment, order)

        order_line_data = [
            OrderLineData(order_line_id=1, order_line_quantity=2),
            OrderLineData(order_line_id=2, order_line_quantity=1)
        ]

        return_order = service.create_return(
            order_number='TESTORDER', return_reason='Niet tevreden', refund_amount=40, order_line_data=order_line_data)
        
        service.approve_return_order(return_order.id)

        pending_return_order = service.process_return_order(return_order.id)

        self.assertEqual(pending_return_order.status, "pending")

    def test_create_return(self):
        service = ReturnService(MockPaymentClient())

        order_line_data = [
            OrderLineData(order_line_id=1, order_line_quantity=2),
            OrderLineData(order_line_id=2, order_line_quantity=1)
        ]

        return_order = service.create_return(
            order_number='TESTORDER', return_reason='Niet tevreden', refund_amount=40, order_line_data=order_line_data)

        self.assertEqual(return_order.order.order_number, 'TESTORDER')
        self.assertEqual(return_order.return_order_lines.count(), 2)

    def test_already_bigger_quantity_than_possible(self):
        service = ReturnService(MockPaymentClient())

        order_line_data = [
            OrderLineData(order_line_id=1, order_line_quantity=2),
        ]

        service.create_return(order_number='TESTORDER',
                              return_reason='Niet tevreden', refund_amount=40, order_line_data=order_line_data)

        order_line_data_new = [
            OrderLineData(order_line_id=1, order_line_quantity=2),
        ]

        with self.assertRaises(Exception):
            service.create_return(order_number='TESTORDER', return_reason='Niet tevreden alweer',
                                  refund_amount=40, order_line_data=order_line_data_new)

    def test_bigger_than_possible_quantity(self):
        service = ReturnService(MockPaymentClient())

        order_line_data = [
            OrderLineData(order_line_id=1, order_line_quantity=99),
        ]

        with self.assertRaises(Exception):
            service.create_return(
                order_number='TESTORDER', return_reason='Niet tevreden', order_line_data=order_line_data)

    def test_order_creation(self):
        order = Order.objects.get(order_number='TESTORDER')

        self.assertEqual(order.order_lines.count(), 2)

        self.assertEqual(order.total_price, 100.00)

        order_line1 = order.order_lines.first()
        self.assertEqual(order_line1.product.name, 'Product 1')
        self.assertEqual(order_line1.quantity, 2)
        self.assertEqual(order_line1.unit_price, 25.00)
        self.assertEqual(order_line1.total_price, 50.00)

        order_line2 = order.order_lines.last()
        self.assertEqual(order_line2.product.name, 'Product 2')
        self.assertEqual(order_line2.quantity, 1)
        self.assertEqual(order_line2.unit_price, 35.00)
        self.assertEqual(order_line2.total_price, 35.00)
