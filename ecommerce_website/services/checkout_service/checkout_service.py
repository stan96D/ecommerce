from ecommerce_website.models import Order, OrderLine, Product
from ecommerce_website.classes.model.order_info import OrderInfo
from ecommerce_website.classes.model.payment_info import PaymentInfo
from ecommerce_website.classes.model.delivery_info import DeliveryInfo
from ecommerce_website.classes.model.shopping_cart import SessionShoppingCart


class CheckoutService:
    def create_order(self, order_info: OrderInfo, payment_info: PaymentInfo, delivery_info: DeliveryInfo, shopping_cart: SessionShoppingCart):
        order = self._create_order(
            order_info, payment_info, delivery_info, shopping_cart)
        self._create_order_lines(order, shopping_cart)
        return order

    def _create_order(self, order_info, payment_info, delivery_info, shopping_cart):

        total_price = shopping_cart.total_price 
        sub_price = shopping_cart.sub_total 
        tax_price_low = shopping_cart.total_tax(9)
        tax_price_high = shopping_cart.total_tax(21)
        shipping_cost = shopping_cart.shipping_price

        return Order.objects.create(
            first_name=order_info.contact_info.first_name,
            last_name=order_info.contact_info.last_name,
            email=order_info.contact_info.email,
            phone=order_info.contact_info.phonenumber,

            payment_information=payment_info.payment_information,
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

            unit_price = product.price
            total_price = unit_price * quantity

            OrderLine.objects.create(
                product=product,
                quantity=quantity,
                unit_price=unit_price,
                total_price=total_price,
                order=order
            )
