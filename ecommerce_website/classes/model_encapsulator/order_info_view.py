
class OrderInfoView:
    def __init__(self, first_name, last_name, email, phone, address, house_number, city, postal_code, country, salutation, billing_address, billing_house_number, billing_city, billing_postal_code, billing_country):

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.address = address
        self.house_number = house_number
        self.city = city
        self.postal_code = postal_code
        self.country = country
        self.salutation = salutation
        self.billing_address = billing_address
        self.billing_house_number = billing_house_number
        self.billing_city = billing_city
        self.billing_postal_code = billing_postal_code
        self.billing_country = billing_country
        self.alternate_billing = 'true' if billing_address not in [
            None, ''] else 'false'
