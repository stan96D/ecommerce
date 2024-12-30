from ecommerce_website.classes.model.account_order_details import OrderDetails
from ecommerce_website.classes.model.address_info import AddressInfo
from ecommerce_website.models import Order, OrderLine
from ecommerce_website.services.order_service.base_order_service import OrderServiceInterface
from django.db.models import F, Q, Prefetch, Sum
from django.db.models.functions import Coalesce
from datetime import timedelta
from django.utils import timezone


class OrderService(OrderServiceInterface):
    @staticmethod
    def get_order_by_id(order_id):
        try:
            return Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return None

    @staticmethod
    def get_order_by_token(token, public=False):
        try:
            if public:
                # Check for token and account being None
                return Order.objects.get(token=token, account=None)
            else:
                # Standard check for token only
                return Order.objects.get(token=token)
        except Order.DoesNotExist:
            return None

    @staticmethod
    def get_account_order_details(order_id):
        # Retrieve the order from the database
        order = OrderService.get_order_by_id(order_id)

        if order is None:
            return None

        # Parse the shipping address
        shipping_details = AddressInfo.destructure_address(
            order.shipping_address)

        if not shipping_details:
            return None

        # Create an order details object
        order_details = OrderDetails(
            order_number=order.order_number,
            first_name=order.first_name,
            last_name=order.last_name,
            email=order.email,
            address=shipping_details.address,
            house_number=shipping_details.house_number,
            city=shipping_details.city,
            postal_code=shipping_details.postal_code,
            country=shipping_details.country,
            phone=order.phone,
        )

        return order_details

    @staticmethod
    def can_order_line_be_returned(order_line_id: str, quantity: int):
        """
        Check if the specified quantity can be returned for an OrderLine.
        :param order_line_id: The ID of the OrderLine.
        :param quantity: The quantity to check for return eligibility.
        :return: True if the quantity can be returned without exceeding the OrderLine quantity, False otherwise.
        """
        try:
            # Annotate the OrderLine with the total returned quantity and include the new quantity in the check
            order_line = OrderLine.objects.filter(id=order_line_id).annotate(
                return_quantity_sum=Coalesce(
                    Sum('return_order_lines__quantity'), 0) + quantity
            ).filter(
                # Ensure total return quantity does not exceed the line quantity
                Q(return_quantity_sum__lte=F('quantity'))
            ).exists()

            return order_line  # Returns True if the line exists and is eligible, False otherwise

        except OrderLine.DoesNotExist:
            # Handle the case where the OrderLine does not exist
            return False

    @staticmethod
    def validate_return_order_lines():
        return

    @staticmethod
    def get_order_with_returnable_lines(order_id):
        try:
            # Define the filtered prefetch queryset for OrderLine
            # We will check if the sum of the quantities in return_order_lines does not match the quantity of order_line
            order_lines_query = OrderLine.objects.filter(order_id=order_id).annotate(
                return_quantity_sum=Sum('return_order_lines__quantity')
            ).filter(
                Q(return_quantity_sum__isnull=True) | Q(
                    return_quantity_sum__lt=F('count_delivered'))
            ).filter(Q(count_delivered__gt=0))

            # Fetch the order with prefetch related filtered order lines
            order = Order.objects.prefetch_related(
                Prefetch('order_lines', queryset=order_lines_query)
            ).get(id=order_id)

            return order
        except Order.DoesNotExist:
            return None

    @staticmethod
    def is_order_returnable(order_id):
        try:

            # Query the order and check for order lines with matching return quantities
            order = Order.objects.get(
                id=order_id,
                order_status__in=['delivered', 'partly'])

            now = timezone.now().date()

            allowed_time_window = now - timedelta(days=14)

            # Check if the order's delivery_date is within the allowed time window
            if order.deliver_date < allowed_time_window:
                return False
            # Get all the order lines for the given order
            order_lines = OrderLine.objects.filter(order=order)

            # Loop through each order line and check the sum of associated return order lines
            for order_line in order_lines:
                # Calculate the total quantity of the return order lines associated with this order line
                total_returned_quantity = order_line.return_order_lines.aggregate(
                    total_returned=Sum('quantity')
                    # Use 0 if no return order lines are associated
                )['total_returned'] or 0

                # If the total returned quantity matches the order line's quantity, it is fully returned
                if total_returned_quantity < order_line.count_delivered:
                    # As soon as we find a line that is not fully returned, we return True (returnable)
                    return True

            # If we get through all the order lines and none are fully returned, return False (not returnable)
            return False

        except Order.DoesNotExist:
            # In case the order doesn't exist or the order is not delivered(no return possible)
            return False

    @staticmethod
    def get_all_orders():
        try:
            return Order.objects.all()
        except Order.DoesNotExist:
            return None

    @staticmethod
    def get_orders_by_account(account):
        try:
            return Order.objects.filter(account=account).order_by('-created_date')
        except Order.DoesNotExist:
            return None

    @staticmethod
    def update_payment_status(payment_id, status):
        try:
            order = Order.objects.get(payment_id=payment_id)

            order.payment_status = status
            if status == "paid":
                order.order_status = "paid"
            elif status == "failed":
                order.order_status = "failed"
            elif status == "canceled":
                order.order_status = "failed"
            elif status == "expired":
                order.order_status = "failed"
            else:
                order.order_status = "open"

            order.save()
            return order
        except Order.DoesNotExist:
            return None

    @staticmethod
    def add_payment(payment, order):
        try:

            order = Order.objects.get(id=order.id)

            order.payment_id = payment['id']
            order.payment_status = payment['status']
            order.payment_url = payment['_links']['checkout']['href']

            order.save()
            return order
        except Order.DoesNotExist:
            return None
