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
