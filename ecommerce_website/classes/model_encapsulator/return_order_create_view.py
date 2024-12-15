from decimal import Decimal, ROUND_HALF_UP
from decimal import Decimal


class ReturnOrderCreateView:
    def __init__(self, order):
        self.order_id = order.id
        self.return_order_lines = []

        for return_order_line in order.order_lines.all():
            self.return_order_lines.append(
                ReturnOrderLineCreateView(return_order_line))


class ReturnOrderLineCreateView:
    def __init__(self, order_line):

        self.id = order_line.id
        self.product_id = order_line.product.id
        self.unit_price = order_line.unit_price
        self.quantity = order_line.count_delivered - \
            order_line.accumulated_return_quantity()
        self.name = order_line.product.name
        self.tax = order_line.product.tax

        if order_line.product.thumbnail and order_line.product.thumbnail.url:
            self.thumbnail_url = order_line.product.thumbnail.url
        else:
            self.thumbnail_url = "/static/images/no_image_placeholder.png"

            # Calculate tax
        self.tax_amount = self.calculate_tax()

    def calculate_tax(self):
        """
        Calculates the tax for the order line and rounds to two decimals.
        Formula: unit_price * (tax / 100)
        """
        tax_amount = self.unit_price * (self.tax / Decimal('100'))
        # Round to two decimal places
        return tax_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
