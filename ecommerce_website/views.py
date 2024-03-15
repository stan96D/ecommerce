from django.shortcuts import render
from ecommerce_website.services.product_service.product_service import ProductService
from django.shortcuts import redirect
from ecommerce_website.models import Product, ProductAttribute
from ecommerce_website.services.shopping_cart_services.shopping_cart_service import ShoppingCartService
from ecommerce_website.handlers.cart_handler import CartHandler

def home(request):
    return render(request, "home.html")

def cart(request):

    cartHandler = CartHandler(request)

    items = cartHandler.data

    return render(request, "cart.html", {'items': items})

def products(request):
    products = ProductService.get_all_products()
    return render(request, 'products.html', {'products': products})


def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        cartService = ShoppingCartService(request)
        cartService.add_item(product.id)
    return redirect('products')
