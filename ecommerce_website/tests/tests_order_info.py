from django.test import TestCase, RequestFactory
from ecommerce_website.classes.model.order_info import OrderInfo
from ecommerce_website.classes.model.contact_info import ContactInfo
from ecommerce_website.classes.model.address_info import AddressInfo
from ecommerce_website.services.order_info_service.order_info_service import OrderInfoService
from ecommerce_website.tests.session_to_request import add_session_to_request

class OrderInfoServiceTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.request1 = self.factory.get('/')
        add_session_to_request(self.request1)

        self.request2 = self.factory.get('/')
        add_session_to_request(self.request2)

        self.contact_info_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phonenumber': '1234567890'
        }
        self.billing_address_data = {
            'address': 'Main St',
            'house_number': '123',
            'city': 'Anytown',
            'postal_code': '12345',
            'country': 'US'
        }
        self.delivery_address_data = {
            'address': 'Main St',
            'house_number': '123',
            'city': 'Anytown',
            'postal_code': '12345',
            'country': 'US'
        }

        self.contact_info = ContactInfo(**self.contact_info_data)
        self.billing_address_info = AddressInfo(**self.billing_address_data)
        self.delivery_address_info = AddressInfo(**self.delivery_address_data)

    def test_create_order(self):
        service = OrderInfoService(self.request1)
        order = service.create_order(
            self.contact_info, self.billing_address_info, self.delivery_address_info)

        self.assertEqual(order.contact_info, self.contact_info)
        self.assertEqual(order.billing_address_info, self.billing_address_info)
        self.assertEqual(order.delivery_address_info,
                         self.delivery_address_info)

    def test_get_order(self):
        self.request1.session['order'] = {
            'contact_info': self.contact_info_data,
            'billing_address_info': self.billing_address_data,
            'delivery_address_info': self.delivery_address_data
        }

        service = OrderInfoService(self.request1)
        order = service.get_order()

        self.assertIsNotNone(order)
        self.assertIsInstance(order, OrderInfo)
        self.assertEqual(order.contact_info.first_name, self.contact_info.first_name)
        self.assertEqual(order.contact_info.last_name,
                         self.contact_info.last_name)
        self.assertEqual(order.billing_address_info.address,
                         self.billing_address_info.address)
        self.assertEqual(order.delivery_address_info.address,
                         self.delivery_address_info.address)


    def test_update_order(self):
        service = OrderInfoService(self.request1)
        service.create_order(
            self.contact_info, self.billing_address_info, self.delivery_address_info)

        new_contact_info = ContactInfo(
            first_name='Jane', last_name='Doe', email='jane@example.com', phonenumber='0987654321'
        )
        new_billing_address_info = AddressInfo(
            address='Main St', house_number='123', city='Anytown', postal_code='12345', country='US'
        )
        new_delivery_address_info = AddressInfo(
            address='Main St', house_number='123', city='Anytown', postal_code='12345', country='US'
        )

        updated_order = service.update_order(
            new_contact_info, new_billing_address_info, new_delivery_address_info)

        self.assertIsInstance(updated_order, OrderInfo)
        self.assertEqual(updated_order.contact_info.first_name, 'Jane')
        self.assertEqual(updated_order.contact_info.last_name, 'Doe')
        self.assertEqual(updated_order.contact_info.email, 'jane@example.com')
        self.assertEqual(updated_order.contact_info.phonenumber, '0987654321')
        self.assertEqual(updated_order.billing_address_info.address, 'Main St')
        self.assertEqual(updated_order.billing_address_info.house_number, '123')
        self.assertEqual(updated_order.billing_address_info.city, 'Anytown')
        self.assertEqual(updated_order.billing_address_info.postal_code, '12345')
        self.assertEqual(updated_order.billing_address_info.country, 'US')
        self.assertEqual(updated_order.delivery_address_info.address, 'Main St')
        self.assertEqual(updated_order.delivery_address_info.house_number, '123')
        self.assertEqual(updated_order.delivery_address_info.city, 'Anytown')
        self.assertEqual(updated_order.delivery_address_info.postal_code, '12345')
        self.assertEqual(updated_order.delivery_address_info.country, 'US')

    def test_delete_order(self):
        self.request1.session['order'] = {
            'contact_info': self.contact_info_data,
            'billing_address_info': self.billing_address_data,
            'delivery_address_info': self.delivery_address_data
        }

        service = OrderInfoService(self.request1)
        service.delete_order()

        self.assertNotIn('order', self.request1.session)

    def test_order_not_shared_between_requests(self):
        service1 = OrderInfoService(self.request1)
        order1 = service1.create_order(
            self.contact_info, self.billing_address_info, self.delivery_address_info)

        service2 = OrderInfoService(self.request2)
        order2 = service2.get_order()

        self.assertIsNotNone(order1)
        self.assertIsNone(order2)
