import locale
from ecommerce_website.classes.helpers.address_formatter import NewLineAddressFormatter
from ecommerce_website.classes.helpers.payment_method_logo_extractor import MolliePaymentMethodLogoExtractor
from ecommerce_website.classes.managers.payment_manager.mollie_client import MollieClient
import locale


class OrderItemView:
    def __init__(self, order):
        # Set the locale to Dutch
        locale.setlocale(locale.LC_TIME, 'nl_NL.UTF-8')

        self.id = order.id
        self.total_price = order.total_price
        self.deliver_date = "Nog niet"
        self.order_number = order.order_number
        self.order_status = order.order_status
        self.payment_url = order.payment_url
        self.billing_address = NewLineAddressFormatter().format(order.billing_address)
        self.shipping_address = NewLineAddressFormatter().format(order.shipping_address)

        self.payment_information = order.payment_information
        self.payment_logo = MolliePaymentMethodLogoExtractor(MollieClient()).extract(order.payment_information_id)

        if order.payment_status:
            payment_status = order.payment_status.capitalize()
            payment_status_dutch = translate_to_dutch(payment_status)
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


def translate_to_dutch(text):
    translation_dict = {
        'Paid': 'Betaald',
        'Pending': 'In afwachting',
        'Failed': 'Mislukt',
        'Canceled': 'Afgebroken',
    }

    return translation_dict.get(text, text)

class OrderLineItemView:
    def __init__(self, order_line):

        attributes_dict = {}
        for attribute in order_line.product.attributes.all():
            attributes_dict[attribute.attribute_type.name] = attribute.value
        print(order_line.total_price, order_line.unit_price)
        self.id = order_line.id
        self.product_id = order_line.product.id
        self.total_price = order_line.total_price
        self.unit_price = order_line.unit_price
        self.quantity = order_line.quantity
        self.name = order_line.product.name
        if order_line.product.thumbnail and order_line.product.thumbnail.url:
            self.thumbnail_url = order_line.product.thumbnail.url

        else:
            self.thumbnail_url = "/static/images/no_image_placeholder.png"
        self.description = attributes_dict['Omschrijving']

