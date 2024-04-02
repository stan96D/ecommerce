from ecommerce_website.models import Order, OrderLine, Product
from ecommerce_website.classes.order import OrderInfo, PaymentInfo, DeliveryInfo
from ecommerce_website.classes.shopping_cart import ShoppingCart


class CheckoutService:
    def create_order(self, order_info: OrderInfo, payment_info: PaymentInfo, delivery_info: DeliveryInfo, shopping_cart: ShoppingCart):
        order = self._create_order(order_info, payment_info, delivery_info)
        self._create_order_lines(order, shopping_cart)
        return order

    def _create_order(self, order_info, payment_info, delivery_info):
        print(order_info.delivery_address)

        return Order.objects.create(
            first_name=order_info.contact_info.first_name,
            last_name=order_info.contact_info.last_name,
            email=order_info.contact_info.email,
            phone=order_info.contact_info.phonenumber,

            payment_information=payment_info.payment_information,
            deliver_date=delivery_info.delivery_date,
            deliver_method=delivery_info.delivery_method,

            shipping_address=order_info.delivery_address_info.full_address,
            billing_address=order_info.billing_address_info.full_address
        )

    def _create_order_lines(self, order, shopping_cart):

        for item in shopping_cart.cart_items:
            product_id = item['product_id']
            quantity = item['quantity']

            try:
                product = Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                continue  

            OrderLine.objects.create(
                product=product,
                quantity=quantity,
                order=order
            )
