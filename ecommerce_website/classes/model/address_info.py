class AddressInfo:
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
