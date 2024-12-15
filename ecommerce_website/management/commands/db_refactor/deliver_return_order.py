from django.db import transaction
from django.db.models import F
from dataclasses import dataclass
from datetime import date
from typing import List

from ecommerce_website.models import ReturnOrderLine
from ecommerce_website.services.return_service.return_service import ReturnService


@dataclass
class ReturnOrderLineData:
    count_delivered: int
    return_order_line_id: int


@dataclass
class ReturnOrderInterface:
    delivery_date: date
    return_order_id: int
    return_line_data: List[ReturnOrderLineData]


# Initialize the data
refactor_data = ReturnOrderInterface(
    delivery_date=date.today(),
    return_order_id=20,
    return_line_data=[
        ReturnOrderLineData(
            return_order_line_id=30,
            count_delivered=2
        )
    ]
)


def deliver_return_order_lines(data: ReturnOrderInterface = refactor_data) -> bool:
    """
    Processes the delivery of return order lines and ensures all updates succeed,
    reverting changes if any operation fails.

    Args:
        data (ReturnOrderInterface): Data containing return order and line details.

    Returns:
        bool: True if all operations succeed, False if any operation fails.
    """
    try:
        with transaction.atomic():
            # Retrieve the return order

            return_order = ReturnService.get_return_by_id(data.return_order_id)

            if not return_order:
                print(f"ReturnOrder with ID {data.return_order_id} not found.")
                return False

            if (return_order.status != "paid" or return_order.status != "partly") and return_order.payment_status != "paid":
                print(f"ReturnOrder with ID {data.order_id} cannot be delivered. It has order status {
                      return_order.status} and payment status {return_order.payment_status}. Both need to be paid or partly")
                return False

            # Process each return line
            for return_line in data.return_line_data:
                if not deliver_return_order_line(return_line, data.delivery_date):
                    raise ValueError(f"Failed to deliver ReturnOrderLine {
                                     return_line.return_order_line_id}")

            # Check if all lines in the return order are fully delivered
            all_lines_delivered = not ReturnOrderLine.objects.filter(
                return_order=return_order,
                # Find lines where delivered count is less than the required quantity
                count_delivered__lt=F('quantity')
            ).exists()

            if all_lines_delivered:
                print(f"All return order lines for ReturnOrder {
                      data.return_order_id} are fully delivered.")
                # Optionally update the return order's status
                return_order.status = 'delivered'  # Assuming 'delivered' is a valid status
                return_order.save()
            else:
                print(f"Some return order lines for ReturnOrder {
                      data.return_order_id} are not fully delivered.")
                return_order.status = 'partly'  # Assuming 'delivered' is a valid status
                return_order.save()

            return all_lines_delivered

    except Exception as e:
        print(f"Error delivering return order lines: {e}")
        return False


def deliver_return_order_line(return_line: ReturnOrderLineData, delivery_date: date) -> bool:
    """
    Updates the `count_delivered` of a `ReturnOrderLine` instance based on the provided data.
    Ensures that the delivered count does not exceed the total allowed count.

    Args:
        return_line (ReturnOrderLineData): The data object containing the updated count and the line ID.
        delivery_date (date): The delivery date for the return line.

    Returns:
        bool: True if the update succeeds, False otherwise.
    """
    try:
        # Retrieve the instance to update
        return_order_line = ReturnOrderLine.objects.get(
            id=return_line.return_order_line_id
        )

        # Calculate the new delivered count
        new_count_delivered = return_order_line.count_delivered + return_line.count_delivered

        # Ensure the new count does not exceed the total allowed count
        if new_count_delivered > return_order_line.quantity:
            print(f"Cannot deliver {return_line.count_delivered} items. "
                  f"Exceeds the allowed total of {return_order_line.quantity}.")
            return False

        # Update the `count_delivered`
        return_order_line.count_delivered = new_count_delivered
        return_order_line.delivery_date = delivery_date
        return_order_line.save()

        print(f"Updated ReturnOrderLine {
              return_line.return_order_line_id}: New count_delivered = {new_count_delivered}")
        return True

    except ReturnOrderLine.DoesNotExist:
        print(f"ReturnOrderLine with ID {
              return_line.return_order_line_id} does not exist.")
        return False

    except Exception as e:
        print(f"Error updating ReturnOrderLine {
              return_line.return_order_line_id}: {e}")
        return False
