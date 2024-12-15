from datetime import date
from decimal import Decimal
from sqlite3 import Date
from ecommerce_website.models import *
from ecommerce_website.classes.managers.payment_manager.mollie_client import MollieClient
from ecommerce_website.classes.managers.payment_manager.base_payment_manager import PaymentClient

from django.db import transaction

from ecommerce_website.services.order_service.order_service import OrderService


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

    @staticmethod
    def get_return_by_id(return_id):
        try:
            return ReturnOrder.objects.get(id=return_id)
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

        refund = self.payment_client.refund_payment(
            payment_id, str(return_order.refund_amount))

        if refund['status'] != "pending":
            raise Exception("Payment doesnt have a pending refund")

        return_order.status = "pending"
        return_order.save()
        return return_order

    @staticmethod
    def create_return_order_with_lines(return_order_data, additional_data, payment_info, delivery_info):
        refund_amount = Decimal("0.00")
        sub_price = Decimal("0.00")
        tax_price_low = Decimal("0.00")
        tax_price_high = Decimal("0.00")
        order_lines = []

        order = OrderService.get_order_by_id(return_order_data["order_id"])

        if not order:
            return None

        # Loop through the return line data and accumulate the order lines and refund amount
        for id, quantity_requested in return_order_data["return_line_data"].items():
            try:
                # Get the OrderLine instance
                order_line = OrderLine.objects.get(id=id)
                product = order_line.product

                line_price = product.unit_selling_price * quantity_requested

                order_lines.append({"order_line": order_line, "quantity": quantity_requested,
                                    "price": line_price})

                # Calculate the refund amount for the return
                refund_amount += line_price

                is_tax_low = order_line.product.tax == WebShopConfig.tax_low()
                is_tax_high = order_line.product.tax == WebShopConfig.tax_high()

                # Calculate sub price and taxes
                if is_tax_low:
                    # Convert 9% to 0.09
                    tax_low = line_price * (product.tax / 100)
                    tax_price_low += tax_low
                    sub_price += line_price - tax_low
                elif is_tax_high:
                    # Convert 21% to 0.21
                    tax_high = line_price * (product.tax / 100)
                    tax_price_high += tax_high
                    sub_price += line_price - tax_high
                else:
                    sub_price += line_price  # No tax

            except OrderLine.DoesNotExist:
                return None  # Handle the case where the order line does not exist

        # Now wrap the creation of the ReturnOrder and ReturnOrderLines in a transaction
        try:
            with transaction.atomic():
                # Create the ReturnOrder object
                return_order = ReturnOrder.objects.create(
                    created_date=date.today(),
                    order=order,
                    shipping_amount=return_order_data["shipping_price"],
                    refund_amount=refund_amount,
                    sub_price=sub_price,
                    tax_price_low=tax_price_low,
                    tax_price_high=tax_price_high,
                    reason=additional_data['return_reason'],
                    first_name=additional_data['first_name'],
                    last_name=additional_data['last_name'],
                    email_address=additional_data['email_address'],
                    address=additional_data['address'],
                    house_number=additional_data['house_number'],
                    city=additional_data['city'],
                    postal_code=additional_data['postal_code'],
                    country=additional_data['country'],
                    phone=additional_data['phone'],

                    payment_information=payment_info.payment_information,
                    payment_information_id=payment_info.payment_method_id,
                    payment_issuer=payment_info.bank_id,

                    deliver_date=delivery_info.delivery_date,
                    deliver_method=delivery_info.delivery_method,
                )

                # Create ReturnOrderLine objects for each order line
                for order_line_data in order_lines:
                    ReturnOrderLine.objects.create(
                        return_order=return_order,
                        order_line=order_line_data["order_line"],
                        quantity=order_line_data["quantity"],
                        refund_amount=order_line_data["price"]
                    )

                # If no exception occurs, return the created ReturnOrder
                return return_order

        except Exception as e:
            # In case of any exception, the transaction will be rolled back, and nothing will be saved.
            print(f"Error creating return order: {e}")
            return None  # Return None to indicate failure

    @staticmethod
    def add_payment(payment, return_id):
        try:

            return_order = ReturnOrder.objects.get(id=return_id)

            return_order.payment_id = payment['id']
            return_order.payment_status = payment['status']
            return_order.payment_url = payment['_links']['checkout']['href']

            return_order.save()
            return return_order
        except Order.DoesNotExist:
            return None

    @staticmethod
    def update_payment_status(payment_id, status):
        try:
            return_order = ReturnOrder.objects.get(payment_id=payment_id)

            return_order.payment_status = status
            if status == "paid":
                return_order.status = "paid"
            elif status == "failed":
                return_order.status = "failed"
            elif status == "canceled":
                return_order.status = "failed"
            elif status == "expired":
                return_order.status = "failed"
            else:
                return_order.status = "open"

            return_order.save()
            return return_order
        except ReturnOrder.DoesNotExist:
            return None

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

            created_return_line = ReturnOrderLine.objects.create(
                return_order=return_order, order_line=key, quantity=value)

            if not created_return_line:
                raise Exception("No return line created")

        return return_order
