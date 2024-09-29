from ecommerce_website.models import *
from ecommerce_website.classes.model.order_info import OrderInfo
from ecommerce_website.classes.model.payment_info import PaymentInfo
from ecommerce_website.classes.model.delivery_info import DeliveryInfo
from ecommerce_website.classes.model.base_shopping_cart_service import ShoppingCartInterface
from ecommerce_website.classes.managers.order_number_manager import *


class CheckoutService:
    def create_order(self, account: AbstractBaseUser, order_info: OrderInfo, payment_info: PaymentInfo, delivery_info: DeliveryInfo, shopping_cart: ShoppingCartInterface):
        order = self._create_order(account,
                                   order_info, payment_info, delivery_info, shopping_cart)
        self._create_order_lines(order, shopping_cart)
        return order

    def _create_order(self, account, order_info, payment_info, delivery_info, shopping_cart):

        total_price = shopping_cart.total_price
        sub_price = shopping_cart.sub_total
        tax_price_low = shopping_cart.total_tax(9)
        tax_price_high = shopping_cart.total_tax(21)
        shipping_cost = shopping_cart.shipping_price

        if not account.is_authenticated:
            account = None

        order_number_manager = OrderNumberManager()
        order_number = order_number_manager.generate_order_number()

        return Order.objects.create(

            account=account,
            order_number=order_number,

            salutation=order_info.contact_info.salutation,
            first_name=order_info.contact_info.first_name,
            last_name=order_info.contact_info.last_name,
            email=order_info.contact_info.email,
            phone=order_info.contact_info.phonenumber,

            payment_information=payment_info.payment_information,
            payment_information_id=payment_info.payment_method_id,
            payment_issuer=payment_info.bank_id,

            deliver_date=delivery_info.delivery_date,
            deliver_method=delivery_info.delivery_method,

            shipping_address=order_info.delivery_address_info.full_address,
            billing_address=order_info.billing_address_info.full_address,

            sub_price=sub_price,
            total_price=total_price,
            tax_price_low=tax_price_low,
            tax_price_high=tax_price_high,
            shipping_price=shipping_cost
        )

    def _create_order_lines(self, order, shopping_cart):
        for item in shopping_cart.cart_items:
            product_id = item['product_id']
            quantity = item['quantity']

            try:
                product = Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                continue

            print("Name", product.name, "has: ", product.has_product_sale)
            if product.has_product_sale == True:
                unit_price = product.unit_sale_price
            else:
                unit_price = product.unit_selling_price

            total_price = unit_price * quantity

            print(unit_price, quantity, total_price)

            OrderLine.objects.create(
                product=product,
                quantity=quantity,
                unit_price=unit_price,
                total_price=total_price,
                order=order
            )

    def add_payment(self, payment, order):
        try:

            order = Order.objects.get(id=order.id)

            order.payment_id = payment['id']
            order.payment_status = payment['status']
            order.payment_url = payment['_links']['checkout']['href']

            order.save()
            return order
        except Order.DoesNotExist:
            return None
