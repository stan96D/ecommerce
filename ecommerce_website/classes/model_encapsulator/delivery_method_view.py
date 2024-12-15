class DeliveryMethodView:
    def __init__(self, delivery_method):

        self.name = delivery_method.name
        self.price = delivery_method.price
        self.days = self.create_range_string(delivery_method.delivery_days)
        self.additional_info = delivery_method.additional_info

    def create_range_string(self, value):
        lower_bound = max(value - 1, 0)
        upper_bound = value + 1

        if lower_bound == upper_bound:
            range_string = str(value)
        elif lower_bound == 0:
            range_string = f"0-{upper_bound}"
        else:
            range_string = f"{lower_bound}-{upper_bound}"

        return range_string
