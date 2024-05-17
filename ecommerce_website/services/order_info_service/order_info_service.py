from ecommerce_website.classes.model.order_info import OrderInfo
from ecommerce_website.classes.model.contact_info import ContactInfo
from ecommerce_website.classes.model.address_info import AddressInfo

class OrderInfoService:

    def __init__(self, request):
        self.request = request

    def create_order(self, contact_info, billing_address_info, delivery_address_info):
        new_order = OrderInfo(request=self.request)

        new_order.create_order(contact_info=contact_info,
                               billing_address_info=billing_address_info, delivery_address_info=delivery_address_info)

        return new_order

    def get_order(self):
        order_data = self.request.session.get('order')

        if order_data:
            order = OrderInfo(self.request)

            contact_info_data = order_data.get('contact_info')
            order.contact_info = ContactInfo(
                **contact_info_data) if contact_info_data else None

            billing_address_data = order_data.get('billing_address_info')
            order.billing_address_info = AddressInfo(
                **billing_address_data) if billing_address_data else None

            delivery_address_data = order_data.get('delivery_address_info')
            order.delivery_address_info = AddressInfo(
                **delivery_address_data) if delivery_address_data else None

            return order
        else:
            return None

    def update_order(self, contact_info, billing_address_info, delivery_address_info):
        existing_order = self.get_order(self.request)

        if existing_order:

            existing_order.contact_info = contact_info
            existing_order.billing_address_info = billing_address_info
            existing_order.delivery_address_info = delivery_address_info
            existing_order.save()
            return existing_order
        else:
            return self.create_order(contact_info, billing_address_info, delivery_address_info)
        
    def delete_order(self):
        if 'order' in self.request.session:
            del self.request.session['order']
            self.request.session.modified = True
