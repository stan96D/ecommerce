
class OrderItemView:
    def __init__(self, order):

        self.id = order.id
        self.total_price = order.total_price
        self.deliver_date = "Nog niet"
        self.order_number = order.order_number
        self.created_date = order.created_date
        order_lines = []

        for order_line in order.order_lines.all():
            order_lines.append(OrderLineItemView(order_line))
        
        self.order_lines = order_lines
        # print(self.order_lines)


class OrderLineItemView:
    def __init__(self, order_line):

        self.id = order_line.id
        self.product_id = order_line.product.id
        self.total_price = order_line.total_price
        self.unit_price = order_line.unit_price
        self.quantity = order_line.quantity
        self.name = order_line.product.name
        self.thumbnail = order_line.product.thumbnail
