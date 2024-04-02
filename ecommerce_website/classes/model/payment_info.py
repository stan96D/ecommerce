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
