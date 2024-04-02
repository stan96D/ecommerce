from ecommerce_website.services.product_service.product_service import ProductService
from decimal import Decimal

class ShoppingCart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add_item(self, product_id, quantity):
        product_id = str(product_id)
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
    
    @property
    def sub_total(self):
        subtotal_amount = Decimal(0)
        for product_id, item in self.cart.items():
            product = ProductService.get_product_by_id(product_id)
            if product is not None:
                product_price = product.price
                subtotal_amount += item['quantity'] * product_price
        
        total_tax_low = self.total_tax(9)  # Calculate the total tax
        total_tax_high = self.total_tax(21)  # Calculate the total tax

        total_tax = total_tax_low + total_tax_high

        return (subtotal_amount - total_tax).quantize(Decimal('0.00'))


    def total_tax(self, tax_percentage):
        total_tax_amount = Decimal(0)
        for product_id, item in self.cart.items():
            product = ProductService.get_product_by_id(product_id)
            if product is not None and product.tax == tax_percentage:
                product_price = product.price
                subtotal = item['quantity'] * product_price
                tax_amount = subtotal * (Decimal(tax_percentage) / 100)
                total_tax_amount += tax_amount
        return total_tax_amount.quantize(Decimal('0.00')) 


