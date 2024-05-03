class PaymentIssuer:
    def __init__(self, id, name, image):
        self.id = id
        self.name = name
        self.image = image

    @classmethod
    def from_dict(cls, issuer_dict):
        id = issuer_dict.get('id')
        name = issuer_dict.get('name')
        image = issuer_dict.get('image', {}).get('svg')
        return cls(id, name, image)
