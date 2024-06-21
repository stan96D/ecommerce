from ecommerce_website.classes.managers.payment_manager.payment_issuer import PaymentIssuer

class PaymentMethod:
    def __init__(self, id, description, minimum_amount, maximum_amount, image_url, status, issuers=None):
        self.id = id
        self.description = description
        self.minimum_amount = minimum_amount
        self.maximum_amount = maximum_amount
        self.image_url = image_url
        self.status = status
        self.issuers = issuers if issuers else []

    def __str__(self):
        return f"{self.description} ({self.id})"

    def display_details(self):
        print(f"Payment Method: {self.description} ({self.id})")
        print(f"Minimum Amount: {self.minimum_amount['value']} {
              self.minimum_amount['currency']}")
        if self.maximum_amount:
            print(f"Maximum Amount: {self.maximum_amount['value']} {
                  self.maximum_amount['currency']}")
        else:
            print("No maximum amount")
        print(f"Image URL: {self.image_url}")
        print(f"Status: {self.status}")
        print("Issuers:")
        for issuer in self.issuers:
            print(f" - {issuer.name} ({issuer.id})")

    def add_issuers(self, issuers):
        self.issuers= issuers

    @classmethod
    def from_dict(cls, method_dict):
        id = method_dict.get('id')
        description = method_dict.get('description')
        minimum_amount = method_dict.get('minimumAmount')
        maximum_amount = method_dict.get('maximumAmount')
        image_url = method_dict.get('image', {}).get('size2x')
        status = method_dict.get('status')
        issuers = [PaymentIssuer.from_dict(
            issuer) for issuer in method_dict.get('issuers', [])]
        return cls(id, description, minimum_amount, maximum_amount, image_url, status, issuers)
