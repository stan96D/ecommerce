from datetime import datetime
from ecommerce_website.models import *

class OrderNumberManager:
    

    def generate_order_number(self):
        try:
            last_order = Order.objects.latest('created_date')
            last_order_number = last_order.order_number
            print(last_order.order_number)
            numeric_part = int(last_order_number[-4:])

            incremented_numeric_part = numeric_part + 1

            new_order_number = f'{
                last_order_number[:-4]}{incremented_numeric_part:03d}'
            return new_order_number
        except Order.DoesNotExist:
            today_date = datetime.now().strftime('%y%m%d')
            return f'{today_date}0001'
