from abc import ABC, abstractmethod
from ecommerce_website.models import *
from ecommerce_website.classes.managers.payment_manager.mollie_client import MollieClient
from ecommerce_website.classes.managers.payment_manager.base_payment_manager import PaymentClient

# class BaseReturnService(ABC):


class OrderLineData():

    def __init__(self, order_line_id, order_line_quantity) -> None:
        self.order_line_id = order_line_id
        self.order_line_quantity = order_line_quantity

class ReturnService():

    def __init__(self, payment_client: PaymentClient) -> None:
        self.payment_client = payment_client

    @staticmethod
    def get_all_returns_for_user(account):
        try:
            return ReturnOrder.objects.filter(order__account=account)
        except ReturnOrder.DoesNotExist:
            return None


    def approve_return_order(self, return_order_id):
        return_order = ReturnOrder.objects.get(id=return_order_id)

        if not return_order:
            raise Exception("No return order found")

        if return_order.status == "approved":
            raise Exception("Return order already approved")
        
        return_order.status = "approved"
        return_order.save()

        return return_order

    def process_return_order(self, return_order_id):
        return_order = ReturnOrder.objects.get(id=return_order_id)

        if not return_order:
            raise Exception("No return order found")

        if return_order.status != "approved":
            raise Exception("Return order not approved")
        
        payment_id = return_order.order.payment_id
        payment_status = return_order.order.payment_status

        if not payment_id:
            raise Exception("No associated payment id")

        if not payment_status or payment_status != "paid":
            raise Exception("Order has not been paid")

        refund = self.payment_client.refund_payment(payment_id, str(return_order.refund_amount))

        if refund['status'] != "pending":
            raise Exception("Payment doesnt have a pending refund")

        return_order.status = "pending"
        return_order.save()
        return return_order

    def create_return(self, order_number, return_reason, refund_amount, order_line_data: list[OrderLineData]):
        order_for_return = Order.objects.get(order_number=order_number)

        if not order_for_return:
            raise Exception("No order found")

        existing_order_lines = self.__get_existing_order_lines__(
            order_line_data)

        created_return_order = self.__create_return_order__(
            order_for_return, return_reason, refund_amount, existing_order_lines)

        return created_return_order

    
    def __is_return_possible__(self, order_line, existing_order_line):
        bigger_than_possible = order_line.order_line_quantity > existing_order_line.quantity

        if bigger_than_possible:
            return False

        existing_return_lines = ReturnOrderLine.objects.filter(
                id=existing_order_line.id)
        total_quantity = order_line.order_line_quantity

        for existing_return_line in existing_return_lines:
            total_quantity += existing_return_line.quantity

        bigger_than_possible = total_quantity > existing_order_line.quantity

        if bigger_than_possible:
            return False
        
        return True
    
    def __get_existing_order_lines__(self, order_line_data):
        existing_order_lines = {}
        for order_line in order_line_data:
            existing_order_line = OrderLine.objects.get(
                id=order_line.order_line_id)
            if not existing_order_line:
                raise Exception("No order line found")

            if not self.__is_return_possible__(order_line, existing_order_line):
                raise Exception("Quantity of return order line exceeds.")

            existing_order_lines[existing_order_line] = order_line.order_line_quantity

        return existing_order_lines

    def __create_return_order__(self, order_for_return, return_reason, refund_amount, existing_order_lines):

        return_order = ReturnOrder.objects.create(
            order=order_for_return, reason=return_reason, refund_amount=refund_amount)

        if not return_order:
            raise Exception("No order created")

        for key, value in existing_order_lines.items():

            created_return_line = ReturnOrderLine.objects.create(return_order=return_order, order_line=key, quantity=value)

            if not created_return_line:
                raise Exception("No return line created")
        
        return return_order


        


