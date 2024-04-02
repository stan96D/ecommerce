from abc import ABC, abstractmethod

class Address:
    def __init__(self, address, house_number, city, postal_code, country):
        self.address = address
        self.house_number = house_number
        self.city = city
        self.postal_code = postal_code
        self.country = country

    def serialize(self):
        return {
            'address': self.address,
            'house_number': self.house_number,
            'city': self.city,
            'postal_code': self.postal_code,
            'country': self.country
        }
    
    @property
    def full_address(self):
        if self.house_number:
            return "{}\n{} {}\n{} {}".format(self.address, self.house_number, self.city, self.postal_code, self.country)
        else:
            return "{}\n{} {}\n{}".format(self.address, self.city, self.postal_code, self.country)
        

class ContactInfo:
    def __init__(self, first_name, last_name, email, phonenumber):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phonenumber = phonenumber

    def serialize(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phonenumber': self.phonenumber
        }


class DeliveryInfo:
    def __init__(self, delivery_method, delivery_date):
        self.delivery_method = delivery_method
        self.delivery_date = delivery_date


    def serialize(self):
        return {
            'delivery_method': self.delivery_method,
            'delivery_date': self.delivery_date,
        }

class PaymentInfo:
    def __init__(self, payment_method, bank):
        self.payment_method = payment_method
        self.bank = bank


    def serialize(self):
        return {
            'payment_method': self.payment_method,
            'bank': self.bank,
        }
    
    @property
    def payment_information(self):
        if self.bank:
            return "{}\n{}".format(self.payment_method, self.bank)
        else:
            return "{}".format(self.payment_method)

class OrderInfo:
    def __init__(self, request):
        self.session = request.session

    def create_order(self, contact_info: ContactInfo, billing_address_info: Address, delivery_address_info: Address):

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


class OrderInfoService:

    def __init__(self, request):
        self.request = request

    def create_order(self, contact_info, billing_address_info, delivery_address_info):
        new_order = OrderInfo(request=self.request)
        
        new_order.create_order(contact_info=contact_info,
                          billing_address_info=billing_address_info, delivery_address_info=delivery_address_info)

        return new_order

    def get_order(self, request):
        order_data = request.session.get('order')
        if order_data:
            order = OrderInfo(request)

            contact_info_data = order_data.get('contact_info')
            order.contact_info = ContactInfo(**contact_info_data) if contact_info_data else None
            
            billing_address_data = order_data.get('billing_address_info')
            order.billing_address_info = Address(**billing_address_data) if billing_address_data else None
            
            delivery_address_data = order_data.get('delivery_address_info')
            order.delivery_address_info = Address(**delivery_address_data) if delivery_address_data else None

            return order
        else:
            return None
        
    
    def update_order(self, request, contact_info, billing_address_info, delivery_address_info):
        existing_order = OrderInfo.load_from_session(request)

        if existing_order:
            existing_order.contact_info = contact_info
            existing_order.billing_address_info = billing_address_info
            existing_order.delivery_address_info = delivery_address_info
            existing_order.save()
            return existing_order
        else:
            return self.create_order(request, contact_info, billing_address_info, delivery_address_info)

    






    