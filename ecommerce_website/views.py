from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from ecommerce_website.services.view_service.order_info_view_service import OrderInfoViewService
from ecommerce_website.services.product_service.product_service import ProductService
from django.shortcuts import redirect, render
from django.urls import reverse
from ecommerce_website.services.shopping_cart_service.shopping_cart_service import ShoppingCartService
from ecommerce_website.services.view_service.product_detail_view_service import ProductDetailViewService
from ecommerce_website.services.view_service.product_view_service import ProductViewService
from ecommerce_website.services.shopping_cart_service.shopping_cart_service import ShoppingCartService
from ecommerce_website.services.view_service.cart_item_view_service import CartItemViewService
from ecommerce_website.services.product_category_service.product_category_service import ProductCategoryService
from ecommerce_website.services.product_filter_service.product_filter_service import ProductFilterService
from ecommerce_website.classes.helpers.product_sorter import ProductSorter
from ecommerce_website.classes.model.address_info import AddressInfo
from ecommerce_website.classes.model.contact_info import ContactInfo
from ecommerce_website.classes.model.payment_info import PaymentInfo
from ecommerce_website.classes.model.delivery_info import DeliveryInfo
from ecommerce_website.services.order_info_service.order_info_service import OrderInfoService
from ecommerce_website.services.checkout_service.checkout_service import CheckoutService
from ecommerce_website.services.order_service.order_service import OrderService
from ecommerce_website.services.view_service.cart_view_service import CartViewService
from django.contrib.auth import logout
from django.http import JsonResponse, HttpResponseBadRequest
import json
from django.contrib.auth import authenticate, login
from ecommerce_website.classes.forms.user_creation_form import CustomUserCreationForm
from ecommerce_website.classes.helpers.shopping_cart_merger import *
from ecommerce_website.services.view_service.order_item_view_service import *
from ecommerce_website.classes.managers.payment_manager.mollie_client import *
from ecommerce_website.classes.managers.mail_manager.mail_manager import *
from ecommerce_website.services.store_motivation_service.store_motivation_service import StoreMotivationService
from ecommerce_website.services.view_service.store_motivation_view_service import StoreMotivationViewService

def sign_in(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)

        if user is not None:

            info_service = OrderInfoService(request)
            merger = ShoppingCartMerger()
            to_cart = AccountShoppingCart()

            from_cart = SessionShoppingCart(request)

            merger.merge_from_to(from_cart, to_cart)
            info_service.delete_order(request)

            login(request, user)


            return redirect('home')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid email or password'})
    else:
        return render(request, 'login.html')
    
def home(request):

    headerData = ProductCategoryService().get_all_active_head_product_categories()

    products = ProductService().get_all_runner_products()
    active_categories = ProductCategoryService().get_all_active_head_product_categories()
    
    view_products = ProductViewService().generate(products)
    store_motivations_data = StoreMotivationService.get_all_active_motivations()
    store_motivations = StoreMotivationViewService().generate(store_motivations_data)

    return render(request, "home.html", {'headerData': headerData, 'store_motivations': store_motivations, 'runner_products_data': view_products, 'category_data': active_categories})



def logout_user(request):

    logout(request)

    return redirect('home')

def login_view(request):

    return render(request, "login.html")


def registration_view(request):

    headerData = ProductCategoryService().get_all_active_head_product_categories()

    store_motivations_data = StoreMotivationService.get_all_active_motivations()
    store_motivations = StoreMotivationViewService().generate(store_motivations_data)

    return render(request, "sign_up.html", {'headerData': headerData, 'store_motivations': store_motivations})

def account_view(request):
        
    headerData = ProductCategoryService().get_all_active_head_product_categories()

    user = request.user

    order_service = OrderService()
    orders = order_service.get_orders_by_account(user)
    
    order_view_service = OrderItemViewService()
    order_views = order_view_service.generate(orders)

    store_motivations_data = StoreMotivationService.get_all_active_motivations()
    store_motivations = StoreMotivationViewService().generate(store_motivations_data)

    return render(request, "account.html", {'headerData': headerData, 'orders': order_views, 'store_motivations': store_motivations})

def sign_up(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            user = form.save()
            login(request, user)

            return redirect('home')
   
    else:
        form = CustomUserCreationForm()

    headerData = ProductCategoryService().get_all_active_head_product_categories()

    store_motivations_data = StoreMotivationService.get_all_active_motivations()
    store_motivations = StoreMotivationViewService().generate(store_motivations_data)

    return render(request, 'sign_up.html', {'form': form, 'headerData': headerData, 'store_motivations': store_motivations})

def navigate_checkout(request):

        cart_service = ShoppingCartService(request)

        if not cart_service.is_valid:
            return redirect('cart')

        order_info_service = OrderInfoService(request)

        order = order_info_service.get_order(request)

        if order and order.is_valid():

            return redirect('checkout')

        else:

            return redirect('order_info')


def cart(request):

    headerData = ProductCategoryService().get_all_active_head_product_categories()

    cart_service = ShoppingCartService(request)
    items = cart_service.cart_items

    cart_view = CartViewService().get(cart_service)

    cart_item_view_service = CartItemViewService()
    cart_item_views = cart_item_view_service.generate(items)

    store_motivations_data = StoreMotivationService.get_all_active_motivations()
    store_motivations = StoreMotivationViewService().generate(store_motivations_data)

    return render(request, "cart.html", {'items': cart_item_views, 'headerData': headerData, 'cart': cart_view, 'store_motivations': store_motivations})

def order_info(request):

    headerData = ProductCategoryService().get_all_active_head_product_categories()

    cart_service = ShoppingCartService(request)
    order_info_service = OrderInfoService(request)

    cart_view = CartViewService().get(cart_service)

    if request.method == 'GET':

        if not cart_service.is_valid:
            return redirect('cart')

        info_view = order_info_service.get_order(request)
        info_view_service = OrderInfoViewService()

        user = request.user

        if info_view:

            json_data = info_view.to_json()

            info_data = {
                "first_name": json_data['contact_info']['first_name'],
                "last_name": json_data['contact_info']['last_name'],
                "email": json_data['contact_info']['email'],
                "phone": json_data['contact_info']['phonenumber'],
                "address": json_data['billing_address_info']['address'],
                "house_number": json_data['billing_address_info']['house_number'],
                "city": json_data['billing_address_info']['city'],
                "postal_code": json_data['billing_address_info']['postal_code'],
                "country": json_data['billing_address_info']['country']
            }

            order_info_view = info_view_service.get(info_data)

        elif user.is_authenticated:

            info_data = {
                "first_name": user.first_name, 
                "last_name": user.last_name,
                "email": user.email, 
                "phone": user.phone_number,
                "address": user.address, 
                "house_number": user.house_number, 
                "city": user.city, 
                "postal_code": user.postal_code, 
                "country": user.country, 
            }

            order_info_view = info_view_service.get(info_data)

        else:
            order_info_view = info_view_service.get_single()

        store_motivations_data = StoreMotivationService.get_all_active_motivations()
        store_motivations = StoreMotivationViewService().generate(store_motivations_data)

        return render(request, "checkout.html", {'headerData': headerData, 'cart': cart_view, 'order_info': order_info_view, 'store_motivatins': store_motivations})
    elif request.method == "POST":

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
        billing_address_info = AddressInfo(
            address, house_number, city, postal_code, country)
        shipping_address_info = AddressInfo(
            address, house_number, city, postal_code, country)

        order_info_service.create_order(
                                        contact_info, billing_address_info, shipping_address_info)

        return redirect("navigate_checkout")

def checkout(request):
    
    headerData = ProductCategoryService().get_all_active_head_product_categories()

    order_info_service = OrderInfoService(request)
    cart_service = ShoppingCartService(request)
    
    cart_view = CartViewService().get(cart_service)

    if request.method == 'GET':

        if not cart_service.is_valid:
            return redirect('cart')

        order = order_info_service.get_order(request)

        if order and order.is_valid():

            client = MollieClient()

            issuers = client.get_issuers()

            store_motivations_data = StoreMotivationService.get_all_active_motivations()
            store_motivations = StoreMotivationViewService().generate(store_motivations_data)

            return render(request, "payment.html", {'headerData': headerData, 'cart': cart_view, 'order': order, 'payment_issuers': issuers, 'store_motivations': store_motivations})

        else:

            return redirect('order_info')


def order_detail(request):
    
    order_id = request.GET.get('order_id')

    order_service = OrderService()
    order = order_service.get_order_by_id(order_id)
    
    headerData = ProductCategoryService().get_all_active_head_product_categories()

    store_motivations_data = StoreMotivationService.get_all_active_motivations()
    store_motivations = StoreMotivationViewService().generate(store_motivations_data)

    return render(request, "order_detail.html", {'headerData': headerData, 'order': order, 'store_motivations': store_motivations})


def confirm_order(request):

    if request.method == 'POST':

        cart_service = ShoppingCartService(request)

        if not cart_service.is_valid:
            return redirect('cart')

        issuer_id = request.POST.get('issuer_id')
        issuer_name = request.POST.get('issuer_name')
        payment_method = request.POST.get('payment_method')
        payment_name = request.POST.get('payment_name')
        payment_img = request.POST.get('payment_name')

        order_service = OrderInfoService(request)
        order_info = order_service.get_order(request)

        if not order_info:
            return HttpResponseBadRequest("Order information not found")

        checkout_service = CheckoutService()
        payment_info = PaymentInfo(payment_name, issuer_name)
        delivery_info = DeliveryInfo("Bezorging", "2024-3-30", 5.00)

        account = request.user
        order = checkout_service.create_order(account, order_info, payment_info, delivery_info, cart_service.shopping_cart)
        
        cart_service.clear_cart()
        order_service.delete_order(request)

        redirect_url = 'https://cb2e-2001-1c05-2233-8d00-89d3-33fc-5ae9-6526.ngrok-free.app//order_detail' + \
            f'?order_id={order.id}'
        webhook_url = 'https://cb2e-2001-1c05-2233-8d00-89d3-33fc-5ae9-6526.ngrok-free.app//mollie_webhook/'

        client = MollieClient()
        payment = client.create_payment('EUR', str(
            order.total_price), order.order_number, redirect_url, webhook_url, payment_method, issuer_id)

        OrderService.add_payment(payment, order)

        checkout_url = payment['_links']['checkout']['href']

        client_mail_sender = ClientMailSender()
        admin_mail_sender = AdminMailSender()

        salutation = account.salutation
        first_name = account.first_name
        last_name = account.last_name
        recipient_email = account.email
        order_number = order.order_number
        order_lines = order.order_lines

        print(client_mail_sender.send_order_confirmation(salutation, last_name, recipient_email, order_number, redirect_url))
        print(admin_mail_sender.send_order_confirmation(
            first_name, last_name, order_number, order_lines))

        return redirect(checkout_url)
    

def search_products(request):

    attributes = request.GET.copy()

    isSort = 'tn_sort' in attributes
    isFilter = ('tn_sort' not in attributes and 'q' not in attributes and len(attributes) > 0) or ('tn_sort' in attributes and 'q' not in attributes and len(attributes) > 1) or (
        'tn_sort' not in attributes and 'q' in attributes and len(attributes) > 1) or ('tn_sort' in attributes and 'q' in attributes and len(attributes) > 2)

    if isSort:
        sort_value = attributes.pop('tn_sort', None)[0]

    search = request.GET.get('q')

    products_for_filters = ProductService.get_products_by_search(search)

    if isFilter:
        attributes.pop('q', None)
        products = ProductService.get_products_by_attributes_and_search(
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

    filterData = ProductFilterService().get_products_filters_for_search(products_for_filters)

    store_motivations_data = StoreMotivationService.get_all_active_motivations()
    store_motivations = StoreMotivationViewService().generate(store_motivations_data)

    return render(request, 'products.html', {'products': productViews, 'filterData': filterData, 'headerData': headerData, 'categoryData': categoryData, 'store_motivations': store_motivations})


def runner_products(request):
    category = 'Hardlopers'
    attributes = request.GET.copy()

    isSort = 'tn_sort' in attributes
    isFilter = 'tn_sort' not in attributes and len(
        attributes) > 0 or 'tn_sort' in attributes and len(
        attributes) > 1

    if isSort:
        sort_value = attributes.pop('tn_sort', None)[0]

    if isFilter:
        products = ProductService().get_runner_products_by_attributes(attributes)

        if isSort:
            products = ProductSorter().sort_products_by(products, sort_value)
    else:
        products = ProductService().get_runner_products()

        if isSort:
            products = ProductSorter().sort_products_by(products, sort_value)

    productViewService = ProductViewService()
    productViews = productViewService.generate(products)

    headerData = ProductCategoryService().get_all_active_head_product_categories()

    breadcrumb = [category]

    categoryData = ProductCategoryService().get_product_category_by_name(category)

    filterData = ProductFilterService().get_product_filters_by_category_name(category)

    store_motivations_data = StoreMotivationService.get_all_active_motivations()
    store_motivations = StoreMotivationViewService().generate(store_motivations_data)

    return render(request, 'products.html', {'products': productViews, 'filterData': filterData, 'headerData': headerData, 'categoryData': categoryData, 'breadcrumbs': breadcrumb, 'store_motivations': store_motivations})


def products_by_category(request, category):

    attributes = request.GET.copy()

    isSort = 'tn_sort' in attributes
    isFilter = 'tn_sort' not in attributes and len(
        attributes) > 0 or 'tn_sort' in attributes and len(
        attributes) > 1

    if isSort:
        sort_value = attributes.pop('tn_sort', None)[0]

    categoryData = ProductCategoryService().get_product_category_by_name(category)

    if isFilter:
        products = ProductService.get_products_by_attributes_and_values(
            attributes, categoryData)
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

    filterData = ProductFilterService().get_product_filters_by_category_name(category)

    store_motivations_data = StoreMotivationService.get_all_active_motivations()
    store_motivations = StoreMotivationViewService().generate(store_motivations_data)

    return render(request, 'products.html', {'products': productViews, 'filterData': filterData, 'headerData': headerData, 'categoryData': categoryData, 'breadcrumbs': breadcrumb, 'store_motivations': store_motivations})


def products_by_subcategory(request, category, subcategory):

    attributes = request.GET.copy()

    isSort = 'tn_sort' in attributes
    isFilter = 'tn_sort' not in attributes and len(
        attributes) > 0 or 'tn_sort' in attributes and len(
        attributes) > 1

    if isSort:
        sort_value = attributes.pop('tn_sort', None)[0]

    categoryData = ProductCategoryService().get_product_category_by_name(subcategory)

    if isFilter:
        products = ProductService.get_products_by_attributes_and_values(
            attributes, categoryData)
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

    filterData = ProductFilterService().get_nested_product_filters_by_category_name(
        category, subcategory)
    
    store_motivations_data = StoreMotivationService.get_all_active_motivations()
    store_motivations = StoreMotivationViewService().generate(store_motivations_data)

    return render(request, 'products.html', {'products': productViews, 'filterData': filterData, 'headerData': headerData, 'categoryData': categoryData, 'breadcrumbs': breadcrumb, 'store_motivations': store_motivations})


def products_by_attribute(request, category, subcategory, attribute):

    attributes = request.GET.copy()

    isSort = 'tn_sort' in attributes
    isFilter = 'tn_sort' not in attributes and len(
        attributes) > 0 or 'tn_sort' in attributes and len(
        attributes) > 1

    if isSort:
        sort_value = attributes.pop('tn_sort', None)[0]

    categoryData = ProductCategoryService().get_product_category_by_name(attribute)

    if isFilter:
        products = ProductService.get_products_by_attributes_and_values(
            attributes, categoryData)
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

    filterData = ProductFilterService().get_double_nested_product_filters_by_category_name(
        category, subcategory, attribute)
    
    store_motivations_data = StoreMotivationService.get_all_active_motivations()
    store_motivations = StoreMotivationViewService().generate(store_motivations_data)

    return render(request, 'products.html', {'products': productViews, 'filterData': filterData, 'headerData': headerData, 'categoryData': categoryData, 'breadcrumbs': breadcrumb, 'store_motivations': store_motivations})


def product_detail(request, id=None):

    headerData = ProductCategoryService().get_all_active_head_product_categories()

    product = ProductService().get_product_by_id(id)
    productViewService = ProductDetailViewService()
    productView = productViewService.get(product)

    store_motivations_data = StoreMotivationService.get_all_active_motivations()
    store_motivations = StoreMotivationViewService().generate(store_motivations_data)
    
    return render(request, 'product_detail.html', {'product': productView, 'headerData': headerData, 'store_motivations': store_motivations})


def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity_str = request.POST.get('quantity')

        try:
            quantity = int(quantity_str)
        except (TypeError, ValueError):
            quantity = 1  

        product = ProductService().get_product_by_id(product_id)

        cartService = ShoppingCartService(request)
        cartService.add_item(product.id, quantity)

    return redirect('cart')


def change_quantity_in_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        product_id = data.get('product_id')
        quantity = data.get('quantity')

        product = ProductService().get_product_by_id(product_id)

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


@csrf_exempt
def mollie_webhook(request):
    print("WebHook CALLED!!!!!")
    if request.method == 'POST':
        try:

            client = MollieClient()
            payment_id = request.POST.get('id')

            print("Received Mollie webhook notification: ", payment_id)

            payment = client.get_payment(payment_id)
            payment_id = payment.id

            new_order = OrderService.update_payment_status(
                payment_id, payment.status)

            print(new_order.payment_status)

            return JsonResponse({'status': 'success'})
        except Exception as e:
            print("Error processing Mollie webhook notification:", str(e))
            return JsonResponse({'status': 'error'}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


