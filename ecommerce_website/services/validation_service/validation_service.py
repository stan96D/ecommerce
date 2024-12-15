

from typing import Dict
from ecommerce_website.services.order_service.order_service import OrderService


class ValidationService():

    def validate_return_order_lines(return_order_data: Dict[str, int]) -> bool:
        """
        Validates the return order data for an order.

        Args:
            return_order_data (Dict[str, int]): A dictionary where keys represent unique identifiers
                                                (e.g., order line IDs as strings or integers),
                                                and values represent the quantities to be returned.

        Returns:
            None
        """

        for order_line_id, quantity in return_order_data.items():
            can_be_returned = OrderService.can_order_line_be_returned(order_line_id, quantity)

            if not can_be_returned:
                return False



        return True