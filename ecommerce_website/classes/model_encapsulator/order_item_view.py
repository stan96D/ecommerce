import locale
from ecommerce_website.classes.helpers.address_formatter import NewLineAddressFormatter
from ecommerce_website.classes.helpers.payment_method_logo_extractor import MolliePaymentMethodLogoExtractor
from ecommerce_website.classes.managers.payment_manager.mollie_client import MollieClient
import locale


class OrderItemView:
    def __init__(self, order):
        # Set the locale to Dutch
        locale.setlocale(locale.LC_TIME, 'nl_NL.UTF-8')

        self.token = order.token
        self.id = order.id
        self.total_price = order.total_price
        self.deliver_date = "Nog niet"
        self.order_number = order.order_number
        self.order_status = order.order_status
        self.payment_url = order.payment_url
        self.billing_address = NewLineAddressFormatter().format(order.billing_address)
        self.shipping_address = NewLineAddressFormatter().format(order.shipping_address)

        self.payment_information = order.payment_information
        self.payment_logo = MolliePaymentMethodLogoExtractor(
            MollieClient()).extract(order.payment_information_id)

        if order.payment_status:
            payment_status = order.payment_status.capitalize()
            payment_status_dutch = MollieClient.translate_to_dutch(
                payment_status)
            self.payment_status = payment_status_dutch

        self.total_price = order.total_price
        self.sub_price = order.sub_price
        self.tax_price_low = order.tax_price_low
        self.tax_price_high = order.tax_price_high
        self.shipping_price = order.shipping_price

        self.created_date = order.created_date.strftime("%A %e %B %Y")

        order_lines = []

        for order_line in order.order_lines.all():
            order_lines.append(OrderLineItemView(order_line))

        self.order_lines = order_lines


class OrderLineItemView:
    def __init__(self, order_line):

        self.id = order_line.id
        self.product_id = order_line.product.id
        self.total_price = order_line.total_price
        self.unit_price = order_line.unit_price
        self.quantity = order_line.quantity
        self.name = order_line.product.name
        self.delivery_date = order_line.delivery_date
        self.delivery_count = order_line.count_delivered
        # Fetch the "Omschrijving" attribute and provide a default empty string if not found
        description = order_line.product.attributes.filter(
            attribute_type__name="Omschrijving"
        ).first()

        productType = order_line.product.attributes.filter(
            attribute_type__name="Producttype").first() or None

        if productType.value == "Vloer":
            self.unit = "pak"
        else:
            attribute = order_line.product.attributes.filter(
                attribute_type__name="Eenheid").first()
            self.unit = attribute.value if attribute else "product"

        # Default to empty string if not found
        self.description = description.value if description else ""
        if order_line.product.thumbnail_url:
            self.thumbnail_url = order_line.product.thumbnail_url
        else:
            self.thumbnail_url = "/static/images/no_image_placeholder.png"

        self.determineStatus(order_line)

    def determineStatus(self, order_line):
        if not self.delivery_date:
            self.status = "Nog te leveren"
            self.statusText = f"Nog te leveren {
                self.delivery_count}/{self.quantity}"
            return

        if self.delivery_date:

            return_quantity = order_line.accumulated_return_quantity()

            if return_quantity > 0:
                self.status = "Geretourneerd"

                if return_quantity == self.quantity:
                    self.statusText = "Volledig geretourneerd"
                else:
                    self.statusText = f"Deels geretourneerd {
                        return_quantity}/{self.quantity}"

            else:
                self.status = "Geleverd"

                if self.delivery_count == self.quantity:
                    self.statusText = f"Geleverd op {self.delivery_date}"
                else:
                    self.statusText = f"Deels geleverd {
                        self.delivery_count}/{self.quantity}"
