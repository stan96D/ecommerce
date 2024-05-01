from ecommerce_website.classes.model.address_info import AddressInfo
from ecommerce_website.classes.model.contact_info import ContactInfo


class OrderInfo:
    def __init__(self, request):
        self.session = request.session

    def create_order(self, contact_info: ContactInfo, billing_address_info: AddressInfo, delivery_address_info: AddressInfo):

        self.contact_info = contact_info
        self.billing_address_info = billing_address_info
        self.delivery_address_info = delivery_address_info

        self.session['order'] = {
            'contact_info': self.contact_info.serialize(),
            'billing_address_info': self.billing_address_info.serialize(),
            'delivery_address_info': self.delivery_address_info.serialize(),
        }

        print(self.session['order'])

        self.save()

    @property
    def billing_address(self):
        return self.session.get('order', {}).get('billing_address_info')

    @property
    def delivery_address(self):
        return self.session.get('order', {}).get('delivery_address_info')

    @property
    def contact(self):
        return self.session.get('order', {}).get('contact_info')

    def is_valid(self):

        if self.contact is None:
            return False
        if self.billing_address is None:
            return False
        if self.delivery_address is None:
            return False

        return True

    def save(self):
        self.session.modified = True

    def to_string(self):
        order_string = f"Contact Info: {self.contact}\n"
        order_string += f"Billing Address: {self.billing_address}\n"
        order_string += f"Delivery Address: {self.delivery_address}\n"
        return order_string
    
    def to_json(self):
        order_json = {
            'contact_info': self.contact_info.serialize(),
            'billing_address_info': self.billing_address_info.serialize(),
            'delivery_address_info': self.delivery_address_info.serialize(),
        }
        return order_json

