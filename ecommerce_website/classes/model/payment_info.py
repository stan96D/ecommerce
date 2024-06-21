class PaymentInfo:
    def __init__(self, payment_method, bank, bank_id, payment_method_id):
        self.payment_method = payment_method
        self.payment_method_id = payment_method_id
        self.bank = bank
        self.bank_id = bank_id

    def serialize(self):
        return {
            'payment_method': self.payment_method,    
            'payment_method_id': self.payment_method_id,
            'bank': self.bank,
            'bank_id': self.bank_id
        }

    @property
    def payment_information(self):
        if self.bank:
            return "{}\n{}".format(self.payment_method, self.payment_method_id, self.bank)
        else:
            return "{}".format(self.payment_method, self.payment_method_id)
