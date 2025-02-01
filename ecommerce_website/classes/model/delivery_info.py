from datetime import datetime, date


class DeliveryInfo:
    def __init__(self, delivery_method, delivery_date):
        self.delivery_method = delivery_method

        if isinstance(delivery_date, (date, datetime)):
            self.delivery_date = delivery_date.strftime('%Y-%m-%d')
        elif isinstance(delivery_date, str):
            # Parse the string and format it
            self.delivery_date = datetime.strptime(
                delivery_date, '%d-%m-%Y').strftime('%Y-%m-%d')
        else:
            raise TypeError(
                "delivery_date must be a string in '%d-%m-%Y' format or a date/datetime object")

    def serialize(self):
        return {
            'delivery_method': self.delivery_method,
            'delivery_date': self.delivery_date,
        }
