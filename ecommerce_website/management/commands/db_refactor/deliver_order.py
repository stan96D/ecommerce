from django.db import transaction
from django.db.models import F
from dataclasses import dataclass
from datetime import date
from typing import List

from ecommerce_website.models import OrderLine
from ecommerce_website.services.order_service.order_service import OrderService


@dataclass
class OrderLineData:
    count_delivered: int
    order_line_id: int


@dataclass
class OrderInterface:
    delivery_date: date
    order_id: int
    line_data: List[OrderLineData]


# Initialize the data
refactor_data = OrderInterface(
    delivery_date=date.today(),
    order_id=9,
    line_data=[
        OrderLineData(
            order_line_id=3,
            count_delivered=2
        )
    ]
)


def deliver_order_lines(data: OrderInterface = refactor_data) -> bool:
    """
    Processes the delivery of order lines and ensures all updates succeed,
    reverting changes if any operation fails.

    Args:
        data (OrderInterface): Data containing order and line details.

    Returns:
        bool: True if all operations succeed, False if any operation fails.
    """
    try:
        with transaction.atomic():
            # Retrieve the order

            order = OrderService.get_order_by_id(data.order_id)

            if not order:
                print(f"Order with ID {data.order_id} not found.")
                return False

            if (order.order_status != "paid" or order.order_status != "partly") and order.payment_status != "paid":
                print(f"Order with ID {data.order_id} cannot be delivered. It has order status {
                      order.order_status} and payment status {order.payment_status}. Both need to be paid or partly.")
                return False

            # Process each return line
            for line in data.line_data:
                if not deliver_order_line(line, data.delivery_date):
                    raise ValueError(f"Failed to deliver OrderLine {
                                     line.order_line_id}")

            # Check if all lines in the  order are fully delivered
            all_lines_delivered = not OrderLine.objects.filter(
                order=order,
                # Find lines where delivered count is less than the required quantity
                count_delivered__lt=F('quantity')
            ).exists()

            if all_lines_delivered:
                print(f"All return order lines for Order {
                      data.order_id} are fully delivered.")
                # Optionally update the order's status
                order.order_status = 'delivered'  # Assuming 'delivered' is a valid status
                order.save()
            else:
                print(f"Some order lines for Order {
                      data.order_id} are not fully delivered.")
                order.order_status = 'partly'  # Assuming 'delivered' is a valid status
                order.save()

            return all_lines_delivered

    except Exception as e:
        print(f"Error delivering order lines: {e}")
        return False


def deliver_order_line(line: OrderLineData, delivery_date: date) -> bool:
    """
    Updates the `count_delivered` of a `OrderLine` instance based on the provided data.
    Ensures that the delivered count does not exceed the total allowed count.

    Args:
        line (OrderLineData): The data object containing the updated count and the line ID.
        delivery_date (date): The delivery date for the line.

    Returns:
        bool: True if the update succeeds, False otherwise.
    """
    try:
        # Retrieve the instance to update
        order_line = OrderLine.objects.get(
            id=line.order_line_id
        )

        # Calculate the new delivered count
        new_count_delivered = order_line.count_delivered + line.count_delivered

        # Ensure the new count does not exceed the total allowed count
        if new_count_delivered > order_line.quantity:
            print(f"Cannot deliver {line.count_delivered} items. "
                  f"Exceeds the allowed total of {order_line.quantity}.")
            return False

        # Update the `count_delivered`
        order_line.count_delivered = new_count_delivered
        order_line.delivery_date = delivery_date
        order_line.save()

        print(f"Updated OrderLine {
              line.order_line_id}: New count_delivered = {new_count_delivered}")
        return True

    except OrderLine.DoesNotExist:
        print(f"OrderLine with ID {
              line.order_line_id} does not exist.")
        return False

    except Exception as e:
        print(f"Error updating OrderLine {
              line.order_line_id}: {e}")
        return False
