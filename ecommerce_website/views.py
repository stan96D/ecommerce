from django.shortcuts import render
from ecommerce_website.services.product_service.product_service import ProductService
from django.shortcuts import redirect
from ecommerce_website.models import Product
from ecommerce_website.services.shopping_cart_services.shopping_cart_service import ShoppingCartService
from ecommerce_website.services.product_service.product_view_service import ProductViewService
from ecommerce_website.services.shopping_cart_services.shopping_cart_service import ShoppingCartService
from ecommerce_website.services.shopping_cart_services.cart_item_view_service import CartItemViewService
from ecommerce_website.classes.handlers.product_category_attribute_view_handler import ProductCategoryAttributeViewHandler

from django.http import JsonResponse
import json

def home(request):

    headerData = ProductCategoryAttributeViewHandler().get_serialized_product_category_attribute_views()

    return render(request, "home.html", {'headerData': headerData})

def cart(request):

    cart_service = ShoppingCartService(request)
    items = cart_service.cart_items

    cart_item_view_service = CartItemViewService()
    cart_item_views = cart_item_view_service.generate(items)

    headerData = ProductCategoryAttributeViewHandler().get_serialized_product_category_attribute_views()


    return render(request, "cart.html", {'items': cart_item_views, 'headerData': headerData})

def products(request, attribute):
    print(attribute)
    products = ProductService.get_products_by_attribute(attribute)
    
    productViewService = ProductViewService()
    productViews = productViewService.generate(products)
    
    headerData = ProductCategoryAttributeViewHandler(
    ).get_serialized_product_category_attribute_views()

    

    return render(request, 'products.html', {'products': productViews, 'headerData': headerData})


def products_by_attribute(request, category, attribute):
    print(category, attribute)
    products = ProductService.get_products_by_attribute(attribute)
    
    productViewService = ProductViewService()
    productViews = productViewService.generate(products)

    headerData = ProductCategoryAttributeViewHandler(
    ).get_serialized_product_category_attribute_views()

    return render(request, 'products.html', {'products': productViews, 'headerData': headerData})

def product_detail(request, id=None):

    product = ProductService.get_product_by_id(id)
    productViewService = ProductViewService()
    productView = productViewService.get(product)

    headerData = ProductCategoryAttributeViewHandler(
    ).get_serialized_product_category_attribute_views()

    return render(request, 'product_detail.html', {'product': productView, 'headerData': headerData})


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

    return redirect('cart')


def change_quantity_in_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        product_id = data.get('product_id')
        quantity = data.get('quantity')

        product = Product.objects.get(id=product_id)

        cartService = ShoppingCartService(request)
        cartService.update_quantity(product.id, quantity)
        
        return JsonResponse({'message': 'Product added to cart successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


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

