import pytz  
from datetime import datetime
from django.test import TestCase
from django.utils import timezone
from ecommerce_website.models import Order
from ecommerce_website.classes.managers.order_number_manager import OrderNumberManager


class OrderNumberManagerTest(TestCase):

    def setUp(self):
        self.manager = OrderNumberManager()

    def test_generate_order_number_no_existing_orders(self):
        order_number = self.manager.generate_order_number()
        today_date = datetime.now().strftime('%y%m%d')
        expected_order_number = f'{today_date}0001'
        self.assertEqual(order_number, expected_order_number)

    def test_generate_order_number_with_existing_orders(self):
        order_number = "240615001"

        custom_date_str = '2024-06-15'

        custom_date = datetime.strptime(
            custom_date_str, '%Y-%m-%d').replace(tzinfo=pytz.utc)
        print(order_number)

        Order.objects.create(
            created_date=custom_date,
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='1234567890',
            payment_information='Credit Card',
            deliver_date='2024-06-15',
            deliver_method='Standard Shipping',
            shipping_address='123 Main St, Anytown, USA',
            billing_address='123 Main St, Anytown, USA',
            order_number=order_number,
            total_price=100.00,
            sub_price=85.00,
            tax_price_low=5.00,
            tax_price_high=10.00,
            shipping_price=10.00,
            payment_id='2oxsqDdMPTXFMdzJWBxE9')

        order_number = self.manager.generate_order_number()
        expected_order_number = '240615002'
        self.assertEqual(order_number, expected_order_number)

        # Order.objects.create(
        #     first_name='John',
        #     last_name='Doe',
        #     email='john.doe@example.com',
        #     phone='1234567890',
        #     payment_information='Credit Card',
        #     deliver_date='2024-06-15',
        #     deliver_method='Standard Shipping',
        #     shipping_address='123 Main St, Anytown, USA',
        #     billing_address='123 Main St, Anytown, USA',
        #     order_number='2306070003',
        #     total_price=100.00,
        #     sub_price=85.00,
        #     tax_price_low=5.00,
        #     tax_price_high=10.00,
        #     shipping_price=10.00,
        #     payment_id='2oxsqDdMPTXFMdzJWBxE9')

        # order_number = self.manager.generate_order_number()
        # expected_order_number = '2306070003'
        # self.assertEqual(order_number, expected_order_number)
