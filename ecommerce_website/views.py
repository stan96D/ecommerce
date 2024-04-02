from django.shortcuts import render
from ecommerce_website.services.product_service.product_service import ProductService
from django.shortcuts import redirect
from ecommerce_website.models import Product
from ecommerce_website.services.shopping_cart_services.shopping_cart_service import ShoppingCartService
from ecommerce_website.services.product_service.product_view_service import ProductViewService
from ecommerce_website.services.shopping_cart_services.shopping_cart_service import ShoppingCartService
from ecommerce_website.services.shopping_cart_services.cart_item_view_service import CartItemViewService
from ecommerce_website.services.product_category_service.product_category_service import ProductCategoryService
from ecommerce_website.services.product_category_service.product_filter_service import ProductFilterService
from ecommerce_website.classes.product_sorter import ProductSorter
from ecommerce_website.classes.cart_item_view import CartView
from ecommerce_website.classes.order import ContactInfo, Address, PaymentInfo, DeliveryInfo, OrderInfoService
from ecommerce_website.services.checkout_service.checkout_service import CheckoutService
from ecommerce_website.classes.session_manager import SessionManager

from django.http import JsonResponse
import json

def home(request):

    headerData = ProductCategoryService().get_all_active_head_product_categories()

    return render(request, "home.html", {'headerData': headerData})

def cart(request):

    cart_service = ShoppingCartService(request)
    items = cart_service.cart_items

    cart_view = CartView(cart_service.total_price,
                         cart_service.sub_price,
                         cart_service.tax_price_high,
                         cart_service.tax_price_low)
    
    cart_item_view_service = CartItemViewService()
    cart_item_views = cart_item_view_service.generate(items)

    headerData = ProductCategoryService().get_all_active_head_product_categories()
    print(cart_view.sub_price)
    return render(request, "cart.html", {'items': cart_item_views, 'headerData': headerData, 'cart': cart_view})


def checkout(request):
    
    headerData = ProductCategoryService().get_all_active_head_product_categories()

    order_service = OrderInfoService(request)
    cart_service = ShoppingCartService(request)

    cart_view = CartView(cart_service.total_price,
                            cart_service.sub_price,
                            cart_service.tax_price_high,
                            cart_service.tax_price_low)

    if request.method == 'POST':
        attributes = request.POST.copy()
    
        first_name = attributes.get('first-name')
        last_name = attributes.get('last-name')
        email_address = attributes.get('email-address')
        address = attributes.get('address')
        house_number = attributes.get('house-number')
        city = attributes.get('city')
        postal_code = attributes.get('postal-code')
        country = attributes.get('country')
        phone = attributes.get('phone')

        contact_info = ContactInfo(first_name, last_name, email_address, phone)
        billing_address_info = Address(address, house_number, city, postal_code, country)
        shipping_address_info = Address(
            address, house_number, city, postal_code, country)

        order = order_service.create_order(contact_info, billing_address_info, shipping_address_info)

        return render(request, "payment.html", {'headerData': headerData, 'cart': cart_view, 'order': order})
    else:

        order = order_service.get_order(request)

        print("Order: ", order)

        if order and order.is_valid():

            return render(request, "payment.html", {'headerData': headerData, 'cart': cart_view, 'order': order})

        else:

            headerData = ProductCategoryService().get_all_active_head_product_categories()

            cart_service = ShoppingCartService(request)

            cart_view = CartView(cart_service.total_price,
                                cart_service.sub_price,
                                cart_service.tax_price_high,
                                cart_service.tax_price_low)
            
            return render(request, "checkout.html", {'headerData': headerData, 'cart': cart_view})


def confirm_order(request):

    if request.method == 'POST':
        attributes = request.POST.copy()
        print(attributes)
        headerData = ProductCategoryService().get_all_active_head_product_categories()

        cart_service = ShoppingCartService(request)

        cart_view = CartView(cart_service.total_price,
                            cart_service.sub_price,
                            cart_service.tax_price_high,
                            cart_service.tax_price_low)
        
        order_service = OrderInfoService(request)
        order_info = order_service.get_order(request)

        checkout_service = CheckoutService()
        payment_info = PaymentInfo("iDeal", "Rabobank")
        delivery_info = DeliveryInfo("Bezorging", "2024-3-30")

        order = checkout_service.create_order(order_info, payment_info, delivery_info, cart_service.shopping_cart)

        SessionManager.clear_session(request)

        return render(request, "order_confirmation.html", {'headerData': headerData, 'cart': cart_view, 'order': order})

def search_products(request):

    attributes = request.GET.copy()

    isSort = 'tn_sort' in attributes
    isFilter = ('tn_sort' not in attributes and 'q' not in attributes and len(attributes) > 0) or ('tn_sort' in attributes and 'q' not in attributes and len(attributes) > 1) or ('tn_sort' not in attributes and 'q' in attributes and len(attributes) > 1) or ('tn_sort' in attributes and 'q' in attributes and len(attributes) > 2)

    if isSort:
        sort_value = attributes.pop('tn_sort', None)[0]

    search = request.GET.get('q')
    print('filter:', isFilter, 'sort:', isSort, 'search:', search)

    if isFilter:
        products = ProductService.get_products_by_attributes_and_values(
            attributes, search)
        if isSort:
            products = ProductSorter().sort_products_by(products, sort_value)
    else:
        products = ProductService.get_products_by_search(search)

        if isSort:
            products = ProductSorter().sort_products_by(products, sort_value)

    productViewService = ProductViewService()
    productViews = productViewService.generate(products)

    headerData = ProductCategoryService().get_all_active_head_product_categories()

    category = "Zoeken"

    categoryData = ProductCategoryService().get_product_category_by_name(category)

    filterData = ProductFilterService().get_product_filters_by_category_name(category)

    return render(request, 'products.html', {'products': productViews, 'filterData': filterData, 'headerData': headerData, 'categoryData': categoryData})


def products_by_category(request, category):

    attributes = request.GET.copy()

    isSort = 'tn_sort' in attributes
    isFilter = 'tn_sort' not in attributes and len(
        attributes) > 0 or 'tn_sort' in attributes and len(
        attributes) > 1

    if isSort:
        sort_value = attributes.pop('tn_sort', None)[0]

    if isFilter:
        products = ProductService.get_products_by_attributes_and_values(attributes, category)
        if isSort:
            products = ProductSorter().sort_products_by(products, sort_value)
    else:
        products = ProductService.get_products_by_attribute(category)

        if isSort:
            products = ProductSorter().sort_products_by(products, sort_value)


    productViewService = ProductViewService()
    productViews = productViewService.generate(products)
    
    headerData = ProductCategoryService().get_all_active_head_product_categories()
    
    breadcrumb = [category]
    
    categoryData = ProductCategoryService().get_product_category_by_name(category)

    filterData = ProductFilterService().get_product_filters_by_category_name(category)

    return render(request, 'products.html', {'products': productViews, 'filterData': filterData, 'headerData': headerData, 'categoryData': categoryData, 'breadcrumbs': breadcrumb})


def products_by_subcategory(request, category, subcategory):

    attributes = request.GET.copy()

    isSort = 'tn_sort' in attributes
    isFilter = 'tn_sort' not in attributes and len(
        attributes) > 0 or 'tn_sort' in attributes and len(
        attributes) > 1

    if isSort:
        sort_value = attributes.pop('tn_sort', None)[0]

    if isFilter:
        products = ProductService.get_products_by_attributes_and_values(
            attributes, category)
        if isSort:
            products = ProductSorter().sort_products_by(products, sort_value)
    else:
        products = ProductService.get_products_by_attribute(category)

        if isSort:
            products = ProductSorter().sort_products_by(products, sort_value)

    productViewService = ProductViewService()
    productViews = productViewService.generate(products)

    headerData = ProductCategoryService().get_all_active_head_product_categories()

    breadcrumb = [category, subcategory]

    categoryData = ProductCategoryService().get_product_category_by_name(subcategory)

    filterData = ProductFilterService().get_product_filters_by_category_name(category)

    return render(request, 'products.html', {'products': productViews, 'filterData': filterData, 'headerData': headerData, 'categoryData': categoryData, 'breadcrumbs': breadcrumb})

def products_by_attribute(request, category, subcategory, attribute):

    attributes = request.GET.copy()

    isSort = 'tn_sort' in attributes
    isFilter = 'tn_sort' not in attributes and len(
        attributes) > 0 or 'tn_sort' in attributes and len(
        attributes) > 1

    if isSort:
        sort_value = attributes.pop('tn_sort', None)[0]

    if isFilter:
        products = ProductService.get_products_by_attributes_and_values(
            attributes, attribute)
        if isSort:
            products = ProductSorter().sort_products_by(products, sort_value)
    else:
        products = ProductService.get_products_by_attribute_from_category(attribute, category)

        if isSort:
            products = ProductSorter().sort_products_by(products, sort_value)
    
    productViewService = ProductViewService()
    productViews = productViewService.generate(products)

    headerData = ProductCategoryService().get_all_active_head_product_categories()

    breadcrumb = [category, subcategory, attribute]

    categoryData = ProductCategoryService().get_product_category_by_name(attribute)

    filterData = ProductFilterService().get_product_filters_by_category_name(category)

    return render(request, 'products.html', {'products': productViews, 'filterData': filterData, 'headerData': headerData, 'categoryData': categoryData, 'breadcrumbs': breadcrumb})



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

