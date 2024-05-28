from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from ecommerce_website.services.view_service.order_info_view_service import OrderInfoViewService
from ecommerce_website.services.product_service.product_service import ProductService
from django.shortcuts import redirect, render
from ecommerce_website.services.shopping_cart_service.shopping_cart_service import ShoppingCartService
from ecommerce_website.services.shopping_cart_service.shopping_cart_service import ShoppingCartService
from ecommerce_website.services.product_category_service.product_category_service import ProductCategoryService
from ecommerce_website.services.product_filter_service.product_filter_service import ProductFilterService
from ecommerce_website.classes.helpers.product_sorter import ProductSorter, ProductSorterUtility
from ecommerce_website.classes.model.address_info import AddressInfo
from ecommerce_website.classes.model.contact_info import ContactInfo
from ecommerce_website.classes.model.payment_info import PaymentInfo
from ecommerce_website.classes.model.delivery_info import DeliveryInfo
from ecommerce_website.services.order_info_service.order_info_service import OrderInfoService
from ecommerce_website.services.checkout_service.checkout_service import CheckoutService
from ecommerce_website.services.order_service.order_service import OrderService
from django.http import JsonResponse, HttpResponseBadRequest
import json
from ecommerce_website.classes.forms.user_creation_form import CustomUserCreationForm
from ecommerce_website.classes.helpers.shopping_cart_merger import *
from ecommerce_website.services.view_service.order_item_view_service import *
from ecommerce_website.classes.managers.payment_manager.mollie_client import *
from ecommerce_website.classes.managers.mail_manager.mail_manager import *
from ecommerce_website.classes.managers.authentication_manager.authentication_manager import AuthenticationManager
from ecommerce_website.classes.helpers.view_service_utility import *



def sign_in(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        auth_manager = AuthenticationManager()

        if auth_manager.login(request, email, password):
            return redirect('home')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid email or password'})

    else:
        return render(request, 'login.html')
    
def home(request):
    
    return render(request, "home.html", {'headerData': ViewServiceUtility.get_header_data(), 
                                         'store_motivations': ViewServiceUtility.get_store_motivations(), 
                                         'runner_products_data': ViewServiceUtility.get_runner_products(), 
                                         'category_data': ViewServiceUtility.get_active_categories()})


def logout_user(request):

    auth_manager = AuthenticationManager()
    auth_manager.logout(request)

    return redirect('home')


def login_view(request):

    return render(request, "login.html")


def registration_view(request):

    return render(request, "sign_up.html", {'headerData': ViewServiceUtility.get_header_data(), 
                                            'store_motivations': ViewServiceUtility.get_store_motivations()})


def account_view(request): 

    user = request.user

    return render(request, "account.html", {'headerData': ViewServiceUtility.get_header_data(), 
                                            'orders': ViewServiceUtility.get_orders_by_user(user), 
                                            'store_motivations': ViewServiceUtility.get_store_motivations()})


def sign_up(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user_data = form.save()

            auth_manager = AuthenticationManager()
            auth_manager.login(request, user_data.email, user_data.password)

            return redirect('home')
   
    else:
        form = CustomUserCreationForm()

    return render(request, 'sign_up.html', {'form': form, 
                                            'headerData': ViewServiceUtility.get_header_data(), 
                                            'store_motivations': ViewServiceUtility.get_store_motivations()})


def navigate_checkout(request):

    if not ShoppingCartService(request).is_valid:
        return redirect('cart')

    order = OrderInfoService(request).get_order()

    if order and order.is_valid():
        return redirect('checkout')
    else:
        return redirect('order_info')


def cart(request):

    return render(request, "cart.html", {'items': ViewServiceUtility.get_cart_items_view(request), 
                                         'headerData': ViewServiceUtility.get_header_data(), 
                                         'cart': ViewServiceUtility.get_cart_view(request), 
                                         'store_motivations': ViewServiceUtility.get_store_motivations()})


def order_info(request):

    order_info_service = OrderInfoService(request)

    if request.method == 'GET':

        if not ShoppingCartService(request).is_valid:
            return redirect('cart')

        info_view = order_info_service.get_order()
        info_view_service = OrderInfoViewService()

        user = request.user

        if info_view:

            json_data = info_view.to_json()

            order_info_view = info_view_service.get({
                "first_name": json_data['contact_info']['first_name'],
                "last_name": json_data['contact_info']['last_name'],
                "email": json_data['contact_info']['email'],
                "phone": json_data['contact_info']['phonenumber'],
                "address": json_data['billing_address_info']['address'],
                "house_number": json_data['billing_address_info']['house_number'],
                "city": json_data['billing_address_info']['city'],
                "postal_code": json_data['billing_address_info']['postal_code'],
                "country": json_data['billing_address_info']['country']
            })

        elif user.is_authenticated:

            order_info_view = info_view_service.get({
                "first_name": user.first_name, 
                "last_name": user.last_name,
                "email": user.email, 
                "phone": user.phone_number,
                "address": user.address, 
                "house_number": user.house_number, 
                "city": user.city, 
                "postal_code": user.postal_code, 
                "country": user.country, 
            })

        else:
            order_info_view = info_view_service.get_single()


        return render(request, "checkout.html", {'headerData': ViewServiceUtility.get_header_data(), 
                                                 'cart': ViewServiceUtility.get_cart_view(request), 
                                                 'order_info': order_info_view, 
                                                 'store_motivatins': ViewServiceUtility.get_store_motivations()})
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
        
    if request.method == 'GET':

        if not ShoppingCartService(request).is_valid:
            return redirect('cart')

        order = ViewServiceUtility.get_order_info(request)

        if order and order.is_valid():

            issuers = MollieClient().get_issuers()

            return render(request, "payment.html", {'headerData': ViewServiceUtility.get_header_data(), 
                                                    'cart': ViewServiceUtility.get_cart_view(request), 
                                                    'order': order, 
                                                    'payment_issuers': issuers, 
                                                    'delivery_methods': ViewServiceUtility.get_active_delivery_methods(),
                                                    'store_motivations': ViewServiceUtility.get_store_motivations()})

        else:
            return redirect('order_info')


def order_detail(request):
    
    order_id = request.GET.get('order_id')

    return render(request, "order_detail.html", {'headerData': ViewServiceUtility.get_header_data(), 
                                                 'order': ViewServiceUtility.get_order_by_id(order_id), 
                                                 'store_motivations': ViewServiceUtility.get_store_motivations()})


def confirm_order(request):

    if request.method == 'POST':

        cart_service = ShoppingCartService(request)

        if not cart_service.is_valid:
            return redirect('cart')

        issuer_id = request.POST.get('issuer_id')
        issuer_name = request.POST.get('issuer_name')
        payment_method = request.POST.get('payment_method')
        payment_name = request.POST.get('payment_name')
        delivery_method = request.POST.get('selected_delivery_method')
        delivery_date = request.POST.get('delivery_date')

        order_service = OrderInfoService(request)
        order_info = order_service.get_order()

        if not order_info:
            return HttpResponseBadRequest("Order information not found")

        payment_info = PaymentInfo(payment_name, issuer_name)
        delivery_info = DeliveryInfo(delivery_method, delivery_date)

        account = request.user
        order = CheckoutService().create_order(account, order_info, payment_info, delivery_info, cart_service.shopping_cart)
        
        cart_service.clear_cart()
        order_service.delete_order()

        # For Mollie testing purposes
        redirect_url = 'https://cb2e-2001-1c05-2233-8d00-89d3-33fc-5ae9-6526.ngrok-free.app//order_detail' + \
            f'?order_id={order.id}'
        webhook_url = 'https://cb2e-2001-1c05-2233-8d00-89d3-33fc-5ae9-6526.ngrok-free.app//mollie_webhook/'

        payment = MollieClient().create_payment('EUR', str(
            order.total_price), order.order_number, redirect_url, webhook_url, payment_method, issuer_id)

        OrderService.add_payment(payment, order)

        checkout_url = payment['_links']['checkout']['href']

        ClientMailSender(mail_manager=HTMLMailManager()).send_order_confirmation(account.salutation,
                                                   account.last_name, 
                                                   account.email, 
                                                   order.order_number, 
                                                   redirect_url)
        
        AdminMailSender(mail_manager=HTMLMailManager()).send_order_confirmation(
            account.first_name,
            account.last_name, 
            order.order_number, 
            order.order_lines)

        return redirect(checkout_url)
    

def search_products(request, category = "Zoeken"):

    attributes = request.GET.copy()

    is_sort = ProductSorterUtility.is_sort(attributes)
    is_filter = ProductSorterUtility.is_search_filter(attributes)

    if is_sort:
        sort_value = attributes.pop('tn_sort', None)[0]

    search = request.GET.get('q')

    products_for_filters = ProductService.get_products_by_search(search)

    if is_filter:
        attributes.pop('q', None)
        products = ProductService.get_products_by_attributes_and_search(
            attributes, search)
        if is_sort:
            products = ProductSorter().sort_products_by(products, sort_value)
    else:
        products = ProductService.get_products_by_search(search)

        if is_sort:
            products = ProductSorter().sort_products_by(products, sort_value)

    category_data = ProductCategoryService().get_product_category_by_name(category)

    filter_data = ProductFilterService().get_products_filters_for_search(products_for_filters)

    return render(request, 'products.html', {
        'products': ViewServiceUtility.get_product_views(products),
        'filterData': filter_data,
        'headerData': ViewServiceUtility.get_header_data(),
        'categoryData': category_data,
        'store_motivations': ViewServiceUtility.get_store_motivations()
    })

def runner_products(request, category='Hardlopers'):
    attributes = request.GET.copy()
    is_sort = ProductSorterUtility.is_sort(attributes)
    is_filter = ProductSorterUtility.is_filter(attributes)

    if is_sort:
        sort_value = attributes.pop('tn_sort', None)[0]

    if is_filter:
        products = ProductService().get_runner_products_by_attributes(attributes)
        if is_sort:
            products = ProductSorter().sort_products_by(products, sort_value)
    else:
        products = ProductService().get_runner_products()
        if is_sort:
            products = ProductSorter().sort_products_by(products, sort_value)

    breadcrumb = [category]
    category_data = ProductCategoryService().get_product_category_by_name(category)
    filter_data = ProductFilterService().get_product_filters_by_category_name(category)

    return render(request, 'products.html', {
        'products': ViewServiceUtility.get_product_views(products),
        'filterData': filter_data,
        'headerData': ViewServiceUtility.get_header_data(),
        'categoryData': category_data,
        'breadcrumbs': breadcrumb,
        'store_motivations': ViewServiceUtility.get_store_motivations()
    })


def products_by_category(request, category):

    attributes = request.GET.copy()

    is_sort = ProductSorterUtility.is_sort(attributes)
    is_filter = ProductSorterUtility.is_filter(attributes)

    if is_sort:
        sort_value = attributes.pop('tn_sort', None)[0]

    category_data = ProductCategoryService().get_product_category_by_name(category)

    if is_filter:
        products = ProductService.get_products_by_attributes_and_values(
            attributes, category_data)
        if is_sort:
            products = ProductSorter().sort_products_by(products, sort_value)
    else:
        products = ProductService.get_products_by_attribute(category)

        if is_sort:
            products = ProductSorter().sort_products_by(products, sort_value)

    breadcrumb = [category]

    filter_data = ProductFilterService().get_product_filters_by_category_name(category)

    return render(request, 'products.html', {
        'products': ViewServiceUtility.get_product_views(products),
        'filterData': filter_data,
        'headerData': ViewServiceUtility.get_header_data(),
        'categoryData': category_data,
        'breadcrumbs': breadcrumb,
        'store_motivations': ViewServiceUtility.get_store_motivations()
    })


def products_by_subcategory(request, category, subcategory):

    attributes = request.GET.copy()

    is_sort = ProductSorterUtility.is_sort(attributes)
    is_filter = ProductSorterUtility.is_filter(attributes)

    if is_sort:
        sort_value = attributes.pop('tn_sort', None)[0]

    category_data = ProductCategoryService().get_product_category_by_name(subcategory)

    if is_filter:
        products = ProductService.get_products_by_attributes_and_values(
            attributes, category_data)
        if is_sort:
            products = ProductSorter().sort_products_by(products, sort_value)
    else:
        products = ProductService.get_products_by_attribute(category)

        if is_sort:
            products = ProductSorter().sort_products_by(products, sort_value)

    breadcrumb = [category, subcategory]

    filter_data = ProductFilterService().get_nested_product_filters_by_category_name(
        category, subcategory)
    
    return render(request, 'products.html', {
        'products': ViewServiceUtility.get_product_views(products),
        'filterData': filter_data,
        'headerData': ViewServiceUtility.get_header_data(),
        'categoryData': category_data,
        'breadcrumbs': breadcrumb,
        'store_motivations': ViewServiceUtility.get_store_motivations()
    })


def products_by_attribute(request, category, subcategory, attribute):

    attributes = request.GET.copy()

    is_sort = ProductSorterUtility.is_sort(attributes)
    is_filter = ProductSorterUtility.is_filter(attributes)

    if is_sort:
        sort_value = attributes.pop('tn_sort', None)[0]

    category_data = ProductCategoryService().get_product_category_by_name(attribute)

    if is_filter:
        products = ProductService.get_products_by_attributes_and_values(
            attributes, category_data)
        if is_sort:
            products = ProductSorter().sort_products_by(products, sort_value)
    else:
        products = ProductService.get_products_by_attribute_from_category(attribute, category)

        if is_sort:
            products = ProductSorter().sort_products_by(products, sort_value)

    breadcrumb = [category, subcategory, attribute]

    filter_data = ProductFilterService().get_double_nested_product_filters_by_category_name(
        category, subcategory, attribute)

    return render(request, 'products.html', {
        'products': ViewServiceUtility.get_product_views(products),
        'filterData': filter_data,
        'headerData': ViewServiceUtility.get_header_data(),
        'categoryData': category_data,
        'breadcrumbs': breadcrumb,
        'store_motivations': ViewServiceUtility.get_store_motivations()
    })


def product_detail(request, id=None):

    return render(request, 'product_detail.html', {'product': ViewServiceUtility.get_product_view_by_id(id), 
                                                   'headerData': ViewServiceUtility.get_header_data(), 
                                                   'related_products': ViewServiceUtility.get_related_products(id),
                                                   'store_motivations': ViewServiceUtility.get_store_motivations()})


def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity_str = request.POST.get('quantity')
        pack_quantity = request.POST.get('packs')
        
        try:
            quantity = int(pack_quantity)
        except (TypeError, ValueError):
            quantity = 1  

        product = ProductService().get_product_by_id(product_id)

        ShoppingCartService(request).add_item(product.id, quantity)

    return redirect('cart')


def change_quantity_in_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        product_id = data.get('product_id')
        quantity = data.get('quantity')

        product = ProductService.get_product_by_id(product_id)

        ShoppingCartService(request).update_quantity(product.id, quantity)
        
        return JsonResponse({'message': 'Product added to cart successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def get_cart_count(request):
    cart_count = ShoppingCartService(request).count
    return JsonResponse({'count': cart_count})


def delete_cart_item(request):
      if request.method == 'POST':
        product_id = request.POST.get('id')
        ShoppingCartService(request).remove_item(product_id)
        return redirect('cart') 


@csrf_exempt
def mollie_webhook(request):
    if request.method == 'POST':
        try:

            payment_id = request.POST.get('id')

            print("Received Mollie webhook notification: ", payment_id)

            payment = MollieClient().get_payment(payment_id)
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


