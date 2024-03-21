from django.shortcuts import render
from ecommerce_website.services.product_service.product_service import ProductService
from django.shortcuts import redirect
from ecommerce_website.models import Product
from ecommerce_website.services.shopping_cart_services.shopping_cart_service import ShoppingCartService
from ecommerce_website.services.product_service.product_view_service import ProductViewService
from ecommerce_website.services.shopping_cart_services.shopping_cart_service import ShoppingCartService
from ecommerce_website.services.shopping_cart_services.cart_item_view_service import CartItemViewService
from ecommerce_website.services.product_category_service.product_category_service import ProductCategoryService
from ecommerce_website.services.product_category_service.product_category_attribute_view_service import ProductCategoryViewService


from django.http import JsonResponse
import json

def home(request):

    headerData = ProductCategoryService().get_all_active_head_product_categories()

    return render(request, "home.html", {'headerData': headerData})

def cart(request):

    cart_service = ShoppingCartService(request)
    items = cart_service.cart_items

    cart_item_view_service = CartItemViewService()
    cart_item_views = cart_item_view_service.generate(items)

    headerData = ProductCategoryService().get_all_active_head_product_categories()


    return render(request, "cart.html", {'items': cart_item_views, 'headerData': headerData})

def products_by_category(request, category):

    products = ProductService.get_products_by_attribute(category)
    
    productViewService = ProductViewService()
    productViews = productViewService.generate(products)
    
    headerData = ProductCategoryService().get_all_active_head_product_categories()
    
    breadcrumb = [category]

    return render(request, 'products.html', {'products': productViews, 'headerData': headerData, 'breadcrumbs': breadcrumb})


def products_by_subcategory(request, category, subcategory):

    products = ProductService.get_products_by_attribute(subcategory)

    productViewService = ProductViewService()
    productViews = productViewService.generate(products)

    headerData = ProductCategoryService().get_all_active_head_product_categories()

    breadcrumb = [category, subcategory]

    return render(request, 'products.html', {'products': productViews, 'headerData': headerData, 'breadcrumbs': breadcrumb})

def products_by_attribute(request, category, subcategory, attribute):

    products = ProductService.get_products_by_attribute(attribute)
    
    productViewService = ProductViewService()
    productViews = productViewService.generate(products)

    headerData = ProductCategoryService().get_all_active_head_product_categories()

    breadcrumb = [category, subcategory, attribute]

    return render(request, 'products.html', {'products': productViews, 'headerData': headerData, 'breadcrumbs': breadcrumb})

def product_detail(request, id=None):

    product = ProductService.get_product_by_id(id)
    productViewService = ProductViewService()
    productView = productViewService.get(product)

    headerData = ProductCategoryService().get_all_active_head_product_categories()

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

