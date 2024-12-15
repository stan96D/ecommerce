from enum import Enum


class CachedOrderStatus(Enum):
    EXPIRED = "Verlopen"
    CREATED = "Aangemaakt"
    READY = "Klaar"


class SessionCachedReturnOrder:
    def __init__(self, order_id, return_line_data):
        self.order_id = str(order_id)
        self.return_line_data = return_line_data
        self.shipping_price = 50
        self.total_price = self.shipping_price

    def to_dict(self):
        """
        Convert the cached return order to a dictionary for storage in session.
        """
        return {
            'order_id': self.order_id,
            'return_line_data': self.return_line_data,
            'shipping_price': self.shipping_price,
            'total_price': self.total_price,
        }


class SessionReturnOrderService:
    def __init__(self, request):
        self.session = request.session
        # Initialize cached return orders in the session if they don't exist
        if 'cached_return_orders' not in self.session:
            self.session['cached_return_orders'] = {}

    def get_cached_order_status(self, cached_order):
        """
        Determine the status of the cached return order.
        """
        order_id = str(cached_order.order_id)
        cached_orders = self.session['cached_return_orders']

        if order_id not in cached_orders:
            return CachedOrderStatus.EXPIRED.value

        if "form_data" not in cached_orders[order_id]:
            return CachedOrderStatus.CREATED.value

        return CachedOrderStatus.READY.value

    def get_cached_order(self, order_id):
        """
        Retrieve the cached return order for a specific order_id from the session.
        """
        order_id = str(order_id)
        cached_orders = self.session['cached_return_orders']

        if order_id not in cached_orders:
            return None

        return cached_orders[order_id]

    def add_return_order(self, order_id, return_line_data):
        """
        Add a new return order to the cached return orders in the session.
        """
        order_id = str(order_id)
        cached_orders = self.session['cached_return_orders']

        # Check if the order already exists in the cache, if not, create a new one
        if order_id not in cached_orders:
            cached_orders[order_id] = {}

        return_order = SessionCachedReturnOrder(
            order_id=order_id,
            return_line_data=return_line_data,
        )

        # Create a new SessionCachedReturnOrder and store it in the session
        cached_orders[order_id] = return_order.to_dict()

        self.save()
        return return_order

    def update_form_data(self, order_id, form_data):
        """
        Update the form_data for a specific cached return order and save it in the session.
        """
        order_id = str(order_id)
        cached_orders = self.session['cached_return_orders']

        # Check if the order exists in the cache
        if order_id not in cached_orders:
            return False

        # Update the form_data for the cached order
        cached_order = cached_orders[order_id]
        cached_order['form_data'] = form_data

        # Save the updated cache back to the session
        self.save()
        return True

    def save(self):
        """
        Save the entire cached return orders back to the session.
        """
        self.session.modified = True  # Ensure session changes are saved

    def get_all_orders(self):
        """
        Retrieve all cached return orders from the session.
        """
        return self.session.get('cached_return_orders', {})

    def clear_order(self, order_id):
        """
        Clear the cached return order for the specific order_id.
        """
        cached_orders = self.session['cached_return_orders']
        if order_id in cached_orders:
            del cached_orders[order_id]
            self.save()
