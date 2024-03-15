from django.shortcuts import render
from ecommerce_website.services.product_service.product_service import ProductService
from django.shortcuts import redirect
from ecommerce_website.models import Product
from ecommerce_website.services.shopping_cart_services.shopping_cart_service import ShoppingCartService
from ecommerce_website.handlers.cart_handler import CartHandler
from ecommerce_website.services.product_service.product_view_service import ProductViewService
from ecommerce_website.services.shopping_cart_services.shopping_cart_service import ShoppingCartService
from django.http import JsonResponse

def home(request):
    return render(request, "home.html")

def cart(request):
    cartHandler = CartHandler(request)
    items = cartHandler.data

    return render(request, "cart.html", {'items': items})

def products(request):
    products = ProductService.get_all_products()
    productViewService = ProductViewService()
    productViews = productViewService.generate(products)
    
    return render(request, 'products.html', {'products': productViews})

def product_detail(request, id=None):

    product = ProductService.get_product_by_id(id)
    productViewService = ProductViewService()
    productView = productViewService.get(product)

    return render(request, 'product_detail.html', {'product': productView})


def add_to_cart(request):
    if request.method == 'POST':

        product_id = request.POST.get('product_id')
        quantity_str = request.POST.get('quantity')

        try:
            quantity = int(quantity_str)
        except (TypeError, ValueError):
            quantity = 1  

        product = Product.objects.get(id=product_id)

        cartService = ShoppingCartService(request)
        cartService.add_item(product.id, quantity)

    return redirect('products')


def get_cart_count(request):
    cartService = ShoppingCartService(request)

    cart_count = cartService.count
    return JsonResponse({'count': cart_count})


def delete_cart_item(request):
      if request.method == 'POST':
        product_id = request.POST.get('id')
        cart_service = ShoppingCartService(request)
        cart_service.remove_item(product_id)
        return redirect('cart') 
