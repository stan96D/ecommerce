from datetime import datetime


class DeliveryInfo:
    def __init__(self, delivery_method, delivery_date):
        self.delivery_method = delivery_method
        self.delivery_date = datetime.strptime(
            delivery_date, '%d-%m-%Y').strftime('%Y-%m-%d')

    def serialize(self):
        return {
            'delivery_method': self.delivery_method,
            'delivery_date': self.delivery_date,
        }
