from ecommerce_website.services.product_service.product_service import ProductService

class ShoppingCart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add_item(self, product_id, quantity):
        product_id = str(product_id)
        print(quantity)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0}
        self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove_item(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def update_quantity(self, product_id, quantity):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
            self.save()

    def clear_cart(self):
        self.cart = {}
        self.save()

    def save(self):
        self.session.modified = True

    @property
    def cart_items(self):
        return [
            {'product_id': product_id, 'quantity': item['quantity']}
            for product_id, item in self.cart.items()
        ]

    @property
    def total_price(self):

        total = 0
        for product_id, item in self.cart.items():

            product = ProductService.get_product_by_id(product_id)

            if product is not None:
                product_price = product.price
                subtotal = item['quantity'] * product_price
                total += subtotal
                
        return total
