from django.shortcuts import render
from ecommerce_website.services.product_service.product_service import ProductService
from django.shortcuts import redirect
from ecommerce_website.classes.shopping_cart import ShoppingCart
from ecommerce_website.models import Product


def home(request):
    return render(request, "home.html")


def products(request):
    products = ProductService.get_all_products()
    return render(request, 'products.html', {'products': products})


def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        cart = ShoppingCart(request)
        cart.add_item(product.id)
    return redirect('product_list')
