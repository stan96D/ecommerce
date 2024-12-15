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

    @staticmethod
    def destructure_address(full_address):
        # Split the address by '\n' to separate each line
        lines = full_address.split('\n')

        # Initialize the variables
        address = None
        house_number = None
        postal_code = None
        city = None
        country = None

        if len(lines) >= 3:
            # Split the first line by '&nbsp;' for address and house number
            address_parts = lines[0].split('&nbsp;')
            address = address_parts[0].strip()
            house_number = address_parts[1].strip() if len(
                address_parts) > 1 else ''

            # Split the second line by '&nbsp;' for postal code and city
            postal_city_parts = lines[1].split('&nbsp;')
            postal_code = postal_city_parts[0].strip()
            city = postal_city_parts[1].strip() if len(
                postal_city_parts) > 1 else ''

            # The third line is the country
            country = lines[2].strip()

        return AddressInfo(address, house_number, city, postal_code, country)

    @property
    def full_address(self):
        # Use a separator between address components for easier parsing
        if self.house_number:
            return "{}&nbsp;{} \n{}&nbsp;{} \n{}".format(self.address, self.house_number, self.postal_code, self.city, self.country)
        else:
            return "{} \n{}&nbsp;{} \n{}".format(self.address, self.postal_code, self.city, self.country)
