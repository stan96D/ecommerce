class DeliveryInfo:
    def __init__(self, delivery_method, delivery_date):
        self.delivery_method = delivery_method
        self.delivery_date = delivery_date
        
    def serialize(self):
        return {
            'delivery_method': self.delivery_method,
            'delivery_date': self.delivery_date,
        }
