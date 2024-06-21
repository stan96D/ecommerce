class ReturnOrderView:
    def __init__(self, return_order):
        self.id = return_order.id
        self.order_id = return_order.order.id
        self.status = return_order.status
        self.reason = return_order.reason
        self.return_date = return_order.return_date
        self.refund_amount = return_order.refund_amount
        self.shipping_amount = return_order.shipping_amount
        self.return_order_lines = []

        for return_order_line in return_order.return_order_lines.all():
            self.return_order_lines.append(
                ReturnOrderLineView(return_order_line))


class ReturnOrderLineView:
    def __init__(self, return_order_line):
        self.id = return_order_line.id
        self.order_line_id = return_order_line.order_line.id
        self.quantity = return_order_line.quantity
        self.refund_amount = return_order_line.refund_amount
