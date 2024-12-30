from ecommerce_website.classes.helpers.address_formatter import NewLineAddressFormatter
from ecommerce_website.classes.helpers.payment_method_logo_extractor import MolliePaymentMethodLogoExtractor
from ecommerce_website.classes.managers.payment_manager.mollie_client import MollieClient


class ReturnOrderView:
    def __init__(self, return_order):
        self.id = return_order.id
        self.token = return_order.token

        self.created_date = return_order.created_date.strftime("%A %e %B %Y")
        self.order_number = return_order.order.order_number
        self.order_id = return_order.order.id
        self.status = return_order.status
        self.reason = return_order.reason
        self.return_date = return_order.return_date.strftime("%A %e %B %Y")
        self.refund_amount = return_order.refund_amount
        self.shipping_amount = return_order.shipping_amount
        self.refund_amount = return_order.refund_amount
        self.return_order_lines = []

        for return_order_line in return_order.return_order_lines.all():
            self.return_order_lines.append(
                ReturnOrderLineView(return_order_line))

        self.first_name = return_order.first_name
        self.last_name = return_order.last_name
        self.billing_address = NewLineAddressFormatter().format(
            return_order.billing_address)
        self.shipping_address = NewLineAddressFormatter().format(
            return_order.shipping_address)
        self.payment_information = return_order.payment_information
        self.payment_logo = MolliePaymentMethodLogoExtractor(
            MollieClient()).extract(return_order.payment_information_id)

        if return_order.payment_status:
            payment_status = return_order.payment_status.capitalize()
            payment_status_dutch = MollieClient.translate_to_dutch(
                payment_status)
            self.payment_status = payment_status_dutch

        self.total_price = return_order.refund_amount
        self.sub_price = return_order.sub_price
        self.tax_price_low = return_order.tax_price_low
        self.tax_price_high = return_order.tax_price_high
        self.shipping_price = return_order.shipping_amount

        self.created_date = return_order.created_date.strftime("%A %e %B %Y")


class ReturnOrderLineView:
    def __init__(self, return_order_line):
        self.id = return_order_line.id
        self.token = return_order_line.return_order.token
        self.order_line_id = return_order_line.order_line.id
        self.quantity = return_order_line.quantity
        self.total_price = return_order_line.refund_amount
        self.name = return_order_line.order_line.product.name

        self.product_id = return_order_line.order_line.product.id
        self.unit_price = return_order_line.order_line.unit_price
        # Fetch the "Omschrijving" attribute and provide a default empty string if not found
        description = return_order_line.order_line.product.attributes.filter(
            attribute_type__name="Omschrijving"
        ).first()

        productType = return_order_line.order_line.product.attributes.filter(
            attribute_type__name="Producttype").first() or None

        if productType.value == "Vloer":
            self.unit = "pak"
        else:
            attribute = return_order_line.order_line.product.attributes.filter(
                attribute_type__name="Eenheid").first()
            self.unit = attribute.value if attribute else "product"

        # Default to empty string if not found
        self.description = description.value if description else ""

        if return_order_line.order_line.product.thumbnail and return_order_line.order_line.product.thumbnail.url:
            self.thumbnail_url = return_order_line.order_line.product.thumbnail.url
        else:
            self.thumbnail_url = "/static/images/no_image_placeholder.png"

        self.delivery_date = return_order_line.delivery_date
        self.delivery_count = return_order_line.count_delivered

        self.determineStatus()

    def determineStatus(self):
        if not self.delivery_date:
            self.status = "Nog op te halen"
            self.statusText = f"Nog op te halen {
                self.delivery_count}/{self.quantity}"
            return

        if self.delivery_date:
            self.status = "Opgehaald"
            self.statusText = f"Opgehaald op {self.delivery_date}"
