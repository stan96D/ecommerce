from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from ecommerce_website.classes.forms.return_form import ReturnForm
from ecommerce_website.classes.helpers.progress_view import get_order_progress_phases
from ecommerce_website.classes.model.cached_return_order import SessionReturnOrderService
from ecommerce_website.services.validation_service.validation_service import ValidationService
from ecommerce_website.services.view_service.order_info_view_service import OrderInfoViewService
from ecommerce_website.services.product_service.product_service import ProductService
from django.shortcuts import redirect, render
from ecommerce_website.services.shopping_cart_service.shopping_cart_service import ShoppingCartService
from ecommerce_website.services.shopping_cart_service.shopping_cart_service import ShoppingCartService
from ecommerce_website.services.product_category_service.product_category_service import ProductCategoryService
from ecommerce_website.services.product_filter_service.product_filter_service import ProductFilterService
from ecommerce_website.classes.helpers.product_sorter import ProductSorter, ProductSorterUtility, QueryProductSorter
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
from ecommerce_website.classes.managers.repay_manager.mollie_repay_manager import MollieRepayManager
from django.contrib.auth.decorators import login_required
from ecommerce_website.classes.helpers.token_generator.token_generator import ResetPasswordTokenGenerator
from django.contrib import messages
from ecommerce_website.services.account_service.account_service import AccountService
from ecommerce_website.classes.forms.store_rating_form import StoreRatingForm
from ecommerce_website.classes.managers.url_manager.url_manager import *
import time
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ecommerce_website.classes.helpers.env_loader import *
from ecommerce_website.services.view_service.product_filter_service import ProductFilterViewService

environment = EnvLoader.get_env()
url_manager = EncapsulatedURLManager.get_url_manager(environment)


def sign_in(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        auth_manager = AuthenticationManager()

        if auth_manager.login(request, email, password):
            messages.success(request, 'Succesvol ingelogd!')

            return redirect('home')
        else:
            return render(request, 'login.html', {'error_message': 'De combinatie van e-mailadres en wachtwoord is niet geldig.'})

    else:
        return render(request, 'login.html')


def home(request):

    return render(request, "home.html", {'headerData': ViewServiceUtility.get_header_data(),
                                         'env': environment,
                                         'store_data': ViewServiceUtility.get_current_store_data(),
                                         'store_rating_data': ViewServiceUtility.get_store_rating_data(),
                                         'can_write_review': AccountService.can_write_review(request.user.id),
                                         'payment_methods': ViewServiceUtility.get_payment_methods(),
                                         'store_motivations': ViewServiceUtility.get_store_motivations(),
                                         'runner_products_data': ViewServiceUtility.get_runner_products(),
                                         'brands': ViewServiceUtility.get_all_brands(),
                                         'messages': messages.get_messages(request),
                                         'category_data': ViewServiceUtility.get_active_categories()})


def logout_user(request):

    auth_manager = AuthenticationManager()
    auth_manager.logout(request)

    messages.success(request, 'Succesvol uitgelogd!')

    return redirect('home')


def login_view(request):

    return render(request, "login.html")


def store_rating_view(request):

    return render(request, "store_rating.html", {'headerData': ViewServiceUtility.get_header_data(),
                                                 'env': environment,
                                                 'store_data': ViewServiceUtility.get_current_store_data(),
                                                 'can_write_review': AccountService.can_write_review(request.user.id),
                                                 'payment_methods': ViewServiceUtility.get_payment_methods(),
                                                 'store_motivations': ViewServiceUtility.get_store_motivations(),
                                                 'brands': ViewServiceUtility.get_all_brands(),
                                                 'messages': messages.get_messages(request)})


def create_store_rating(request):

    if request.method == "POST":

        form = StoreRatingForm(request.POST)
        if form.is_valid():
            store_rating = form.save(commit=False)
            store_rating.user = request.user
            store_rating.save()
            return redirect('home')
        else:
            redirect('store_rating_view')


def new_password(request, token):
    print(request)
    if request.method == 'GET':

        is_expired = ResetPasswordTokenGenerator.is_token_expired(token)

        if not is_expired:
            return render(request, "new_password.html", {'token': token})
        else:
            return redirect('home')

    if request.method == 'POST':
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if new_password1 != new_password2:
            return render(request, "new_password.html", {'token': token, 'error_message': "Wachtwoorden komen niet overeen."})

        try:
            uidb64, token = token.split('-', 1)
            uid = urlsafe_base64_decode(uidb64).decode()
            user = Account.objects.get(pk=uid)

            if ResetPasswordTokenGenerator.check_token(user, token):
                user.password = make_password(new_password1)
                user.save()
                return render(request, "login.html", {'success_message': "Wachtwoord succesvol veranderd."})
            else:
                return render(request, "new_password.html", {'token': token, 'error_message': "Ongeldige of verlopen token."})

        except (Account.DoesNotExist, ValueError, TypeError):
            return render(request, "new_password.html", {'token': token, 'error_message': "Ongeldige of verlopen token."})


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = Account.objects.get(email=email)

            ForgotPasswordMailSender(
                HTMLMailManager()).send_password_reset_email(user)

            return render(request, "login.html", {'success_message': "Nieuw wachtwoord aangevraagd."})
        except Account.DoesNotExist:
            return render(request, 'forgot_password.html', {'error_message': 'Geen account met gegeven email gevonden.'})

    elif request.method == 'GET':
        return render(request, "forgot_password.html")


def registration_view(request):

    return render(request, "sign_up.html", {'headerData': ViewServiceUtility.get_header_data(),
                                            'env': environment,
                                            'store_data': ViewServiceUtility.get_current_store_data(),
                                            'payment_methods': ViewServiceUtility.get_payment_methods(),
                                            'brands': ViewServiceUtility.get_all_brands(),
                                            'store_motivations': ViewServiceUtility.get_store_motivations()})


def account_view(request):

    user = request.user

    if (not user.is_authenticated):
        return redirect('login')

    return render(request, "account.html", {'headerData': ViewServiceUtility.get_header_data(),
                                            'env': environment,
                                            'store_data': ViewServiceUtility.get_current_store_data(),
                                            'account': user,
                                            'payment_methods': ViewServiceUtility.get_payment_methods(),
                                            'brands': ViewServiceUtility.get_all_brands(),
                                            'orders': ViewServiceUtility.get_orders_by_user(user),
                                            'returns': ViewServiceUtility.get_return_orders_by_user(user),
                                            'store_motivations': ViewServiceUtility.get_store_motivations()})


@ csrf_protect
def change_account_information(request):
    if request.method == 'POST':
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        user = request.user

        if not first_name and not last_name and not email and not phone:
            return JsonResponse({'status': 'success', 'message': 'Data received successfully'})

        if user.email != email:
            existing_account = len(Account.objects.filter(email=email)) > 0

            if existing_account:
                return JsonResponse({'status': 'fail', 'errors': {'email': 'Dit emailadres is niet beschikbaar.'}}, status=400)

        account = Account.objects.get(email=user.email)

        if first_name:
            account.first_name = first_name

        if last_name:
            account.last_name = last_name

        if email:
            account.email = email

        if phone:
            account.phone_number = phone

        account.save()

        return JsonResponse({'status': 'success', 'message': 'Data received successfully'})

    return JsonResponse({'status': 'fail', 'message': 'Invalid request method'}, status=405)


@ csrf_protect
def change_delivery_address_information(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        house_number = request.POST.get('house_number')
        postal_code = request.POST.get('postal_code')
        city = request.POST.get('city')
        country = request.POST.get('country')

        if not address and not house_number and not postal_code and not city and not country:
            return JsonResponse({'status': 'success', 'message': 'Data received successfully'})

        user = request.user
        account = Account.objects.get(email=user.email)

        if address:
            account.address = address

        if house_number:
            account.house_number = house_number

        if postal_code:
            account.postal_code = postal_code

        if city:
            account.city = city

        if country:
            account.country = country

        account.save()

        return JsonResponse({'status': 'success', 'message': 'Data received successfully'})

    return JsonResponse({'status': 'fail', 'message': 'Invalid request method'}, status=405)


@ login_required
def delete_account(request):
    if request.method == 'DELETE':
        user = request.user
        user.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


def sign_up(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():

            auth_manager = AuthenticationManager()

            message, message_type = auth_manager.sign_up(request, form)

            if message_type == 'success':
                messages.success(request, message)
            elif message_type == 'warning':
                messages.warning(request, message)

            return redirect('home')
        else:
            return render(request, 'sign_up.html', {
                'form': form,
                'headerData': ViewServiceUtility.get_header_data(),
                'env': environment,
                'store_data': ViewServiceUtility.get_current_store_data(),
                'payment_methods': ViewServiceUtility.get_payment_methods(),
                'brands': ViewServiceUtility.get_all_brands(),
                'store_motivations': ViewServiceUtility.get_store_motivations()
            })

    else:
        return redirect('registration')


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
                                         'env': environment,
                                         'store_data': ViewServiceUtility.get_current_store_data(),
                                         'payment_methods': ViewServiceUtility.get_payment_methods(),
                                         'brands': ViewServiceUtility.get_all_brands(),
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
                "salutation": json_data['contact_info']['salutation'],

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
                "salutation": user.salutation,

            })

        else:
            order_info_view = info_view_service.get_single()

        return render(request, "checkout.html", {'headerData': ViewServiceUtility.get_header_data(),
                                                 'env': environment,
                                                 'store_data': ViewServiceUtility.get_current_store_data(),
                                                 'payment_methods': ViewServiceUtility.get_payment_methods(),
                                                 'brands': ViewServiceUtility.get_all_brands(),
                                                 'cart': ViewServiceUtility.get_cart_view(request),
                                                 'order_info': order_info_view,
                                                 'store_motivations': ViewServiceUtility.get_store_motivations()})
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
        salutation = attributes.get('salutation')

        contact_info = ContactInfo(
            first_name, last_name, email_address, phone, salutation)
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

            issuers = MollieClient().get_issuers('ideal')

            return render(request, "payment.html", {'headerData': ViewServiceUtility.get_header_data(),
                                                    'env': environment,
                                                    'store_data': ViewServiceUtility.get_current_store_data(),
                                                    'cart': ViewServiceUtility.get_cart_view(request),
                                                    'payment_methods': ViewServiceUtility.get_payment_methods(),
                                                    'brands': ViewServiceUtility.get_all_brands(),
                                                    'order': order,
                                                    'payment_issuers': issuers,
                                                    'delivery_methods': ViewServiceUtility.get_active_delivery_methods(),
                                                    'store_motivations': ViewServiceUtility.get_store_motivations()})

        else:
            return redirect('order_info')


def order_detail(request):

    order_id = request.GET.get('order_id')

    order = ViewServiceUtility.get_order_by_id(order_id)

    progress_phases = get_order_progress_phases(order.order_status)

    return render(request, "order_detail.html", {'headerData': ViewServiceUtility.get_header_data(),
                                                 'env': environment,
                                                 'store_data': ViewServiceUtility.get_current_store_data(),
                                                 'payment_methods': ViewServiceUtility.get_payment_methods(),
                                                 'brands': ViewServiceUtility.get_all_brands(),
                                                 'progress_phases': progress_phases,
                                                 'order': order,
                                                 'store_motivations': ViewServiceUtility.get_store_motivations()})


def repay_order(request, order_id):

    if request.method == 'POST':

        repayment_manager = MollieRepayManager()
        checkout_url = repayment_manager.repay(order_id, OrderService)

        return redirect(checkout_url)


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

        payment_info = PaymentInfo(
            payment_name, issuer_name, issuer_id, payment_method)
        delivery_info = DeliveryInfo(delivery_method, delivery_date)

        account = request.user
        order = CheckoutService().create_order(account, order_info, payment_info,
                                               delivery_info, cart_service.shopping_cart)

        cart_service.clear_cart()
        order_service.delete_order()

        redirect_url = url_manager.create_redirect(order.id)
        webhook_url = url_manager.create_webhook()

        print(payment_method, issuer_id, issuer_name, payment_name)
        payment = MollieClient().create_payment('EUR', str(
            order.total_price), order.order_number, redirect_url, webhook_url, payment_method, issuer_id)

        OrderService.add_payment(payment, order)

        checkout_url = payment['_links']['checkout']['href']
        print(payment, checkout_url)

        if account.is_authenticated:
            salutation = account.salutation
            last_name = account.last_name
            email = account.email
        else:
            salutation = order.salutation
            last_name = order.last_name
            email = order.email

        ClientMailSender(mail_manager=HTMLMailManager()).send_order_confirmation(salutation,
                                                                                 last_name,
                                                                                 email,
                                                                                 order.order_number,
                                                                                 redirect_url)

        return redirect(checkout_url)


def products(request, category='Assortiment'):

    # Start timing
    start_time = time.time()

    print(f"Starting 'products_by_category' for category: {category}")

    attributes = request.GET.copy()

    is_sort = ProductSorterUtility.is_sort(attributes)
    is_paginated = ProductSorterUtility.is_paginated(attributes)

    if is_paginated:
        page = attributes.pop('page', None)[0]
        print(f"Pagination value detected: {page}")
    else:
        page = 1

    is_filter = ProductSorterUtility.is_filter(attributes)

    if is_sort:
        sort_value = attributes.pop('tn_sort', None)[0]
        print(f"Sort value detected: {sort_value}")

    print(f"Checked sort and pagination flags - Time elapsed: {
          time.time() - start_time:.4f} seconds")

    category_data = ProductCategoryService().get_product_category_by_name(category)
    print(
        f"Retrieved category data - Time elapsed: {time.time() - start_time:.4f} seconds")

    if is_filter:
        selected_option_filters, selected_slider_filters = ProductSorterUtility.create_filters(
            attributes)
        print(
            f"Created filters - Time elapsed: {time.time() - start_time:.4f} seconds")

        combined_filters = {}

        for key, values in selected_option_filters.items():
            combined_filters[key] = list(values)

        for key, values in selected_slider_filters.items():
            combined_filters[key] = list(values)

        products = ProductService.get_filtered_products_by_value_and_category(
            selected_option_filters, selected_slider_filters, category)
        print(
            f"Filtered products by attributes - Time elapsed: {time.time() - start_time:.4f} seconds")

        if is_sort:
            products = QueryProductSorter.sort_by(products, sort_value)
            print(
                f"Sorted products by attribute - Time elapsed: {time.time() - start_time:.4f} seconds")
        else:
            products = QueryProductSorter.sort_default(products)
            print(f"Applied default sorting to products - Time elapsed: {
                  time.time() - start_time:.4f} seconds")
    else:

        products = ProductService.get_products_assortment()

        print(
            f"Fetched products by category - Time elapsed: {time.time() - start_time:.4f} seconds")

        if is_sort:
            products = QueryProductSorter.sort_by(products, sort_value)
            print(
                f"Sorted products by attribute - Time elapsed: {time.time() - start_time:.4f} seconds")
        else:
            products = QueryProductSorter.sort_default(products)
            print(f"Applied default sorting to products - Time elapsed: {
                  time.time() - start_time:.4f} seconds")

    breadcrumb = [category]
    paginator = Paginator(products, 30)

    try:
        paginated_products = paginator.page(page)
    except PageNotAnInteger:
        paginated_products = paginator.page(1)
    except EmptyPage:
        paginated_products = paginator.page(paginator.num_pages)
    print(
        f"Paginated products - Time elapsed: {time.time() - start_time:.4f} seconds")

    page_obj = paginator.get_page(page)

    if is_filter:
        filter_data = ProductFilterService.get_products_filters_by_products(
            products, category, combined_filters)
    else:
        filter_data = ProductFilterService.get_product_filters_by_category(
            category)
    print(
        f"Retrieved filter data - Time elapsed: {time.time() - start_time:.4f} seconds")

    if len(filter_data) > 0:

        price_filter = ProductFilterService.create_filter_for_price(products)

        if is_filter and price_filter.name not in combined_filters:
            # Only add filters that have more than one value
            if price_filter.lowest != price_filter.highest:
                filter_data.append(price_filter)
        else:
            # Always add values that are already a filter
            if price_filter.lowest != price_filter.highest:
                filter_data.append(price_filter)

        print(
            f"Added price filter - Time elapsed: {time.time() - start_time:.4f} seconds")

    if is_filter:
        filter_data = ProductFilterService.sort_product_filters_on_importance(
            filter_data, combined_filters)
    else:
        filter_data = ProductFilterService.sort_product_filters_on_importance(
            filter_data)
    print(
        f"Sorted product filters - Time elapsed: {time.time() - start_time:.4f} seconds")

    product_views = ViewServiceUtility.get_product_views(paginated_products)
    print(
        f"Generated product views - Time elapsed: {time.time() - start_time:.4f} seconds")
    response = render(request, 'products.html', {
        'page_obj': page_obj,
        'products': product_views,
        'filter_data': filter_data,
        'headerData': ViewServiceUtility.get_header_data(),
        'env': environment,
        'store_data': ViewServiceUtility.get_current_store_data(),
        'payment_methods': ViewServiceUtility.get_payment_methods(),
        'brands': ViewServiceUtility.get_all_brands(),
        'categoryData': category_data,
        'breadcrumbs': breadcrumb,
        'store_motivations': ViewServiceUtility.get_store_motivations(),
        'product_count': len(products)
    })
    print(
        f"Rendered template - Total time elapsed: {time.time() - start_time:.4f} seconds")

    return response


def search_products(request, category="Zoeken"):

    # Start timing
    start_time = time.time()

    print(f"Starting 'products_by_category' for category: {category}")

    attributes = request.GET.copy()

    is_sort = ProductSorterUtility.is_sort(attributes)
    is_paginated = ProductSorterUtility.is_paginated(attributes)

    # Safely pop the 'q' parameter and set a default of None
    search = attributes.pop('q', [None])[0] if 'q' in attributes else ""

    if is_paginated:
        page = attributes.pop('page', None)[0]
        print(f"Pagination value detected: {page}")
    else:
        page = 1

    is_filter = ProductSorterUtility.is_search_filter(attributes)

    if is_sort:
        sort_value = attributes.pop('tn_sort', None)[0]
        print(f"Sort value detected: {sort_value}")

    print(f"Checked sort and pagination flags - Time elapsed: {
          time.time() - start_time:.4f} seconds")

    category_data = ProductCategoryService().get_product_category_by_name(category)
    print(
        f"Retrieved category data - Time elapsed: {time.time() - start_time:.4f} seconds")

    combined_filters = {}

    if is_filter:
        selected_option_filters, selected_slider_filters = ProductSorterUtility.create_filters(
            attributes)
        print(
            f"Created filters - Time elapsed: {time.time() - start_time:.4f} seconds")

        for key, values in selected_option_filters.items():
            combined_filters[key] = list(values)

        for key, values in selected_slider_filters.items():
            combined_filters[key] = list(values)

        products = ProductService.get_filtered_products_by_search(
            selected_option_filters, selected_slider_filters, search)
        print(
            f"Filtered products by attributes - Time elapsed: {time.time() - start_time:.4f} seconds")

        if is_sort:
            products = QueryProductSorter.sort_by(products, sort_value)
            print(
                f"Sorted products by attribute - Time elapsed: {time.time() - start_time:.4f} seconds")
        else:
            products = QueryProductSorter.sort_default(products)
            print(f"Applied default sorting to products - Time elapsed: {
                  time.time() - start_time:.4f} seconds")
    else:

        products = ProductService.get_products_by_search(search)

        print(
            f"Fetched products by category - Time elapsed: {time.time() - start_time:.4f} seconds")

        if is_sort:
            products = QueryProductSorter.sort_by(products, sort_value)
            print(
                f"Sorted products by attribute - Time elapsed: {time.time() - start_time:.4f} seconds")
        else:
            products = QueryProductSorter.sort_default(products)
            print(f"Applied default sorting to products - Time elapsed: {
                  time.time() - start_time:.4f} seconds")

    breadcrumb = [category]
    paginator = Paginator(products, 30)

    try:
        paginated_products = paginator.page(page)
    except PageNotAnInteger:
        paginated_products = paginator.page(1)
    except EmptyPage:
        paginated_products = paginator.page(paginator.num_pages)
    print(
        f"Paginated products - Time elapsed: {time.time() - start_time:.4f} seconds")

    page_obj = paginator.get_page(page)

    filter_data = ProductFilterService.get_products_filters_by_products(
        products, category, combined_filters)

    print(
        f"Retrieved filter data - Time elapsed: {time.time() - start_time:.4f} seconds")

    if len(filter_data) > 0:

        price_filter = ProductFilterService.create_filter_for_price(products)

        if is_filter and price_filter.name not in combined_filters:
            # Only add filters that have more than one value
            if price_filter.lowest != price_filter.highest:
                filter_data.append(price_filter)
        else:
            # Always add values that are already a filter
            if price_filter.lowest != price_filter.highest:
                filter_data.append(price_filter)

        print(
            f"Added price filter - Time elapsed: {time.time() - start_time:.4f} seconds")

    if is_filter:
        filter_data = ProductFilterService.sort_product_filters_on_importance(
            filter_data, combined_filters)
    else:
        filter_data = ProductFilterService.sort_product_filters_on_importance(
            filter_data)
    print(
        f"Sorted product filters - Time elapsed: {time.time() - start_time:.4f} seconds")

    response = render(request, 'products.html', {
        'page_obj': page_obj,
        'products': ViewServiceUtility.get_product_views(paginated_products),
        'filter_data': filter_data,
        'headerData': ViewServiceUtility.get_header_data(),
        'env': environment,
        'store_data': ViewServiceUtility.get_current_store_data(),
        'payment_methods': ViewServiceUtility.get_payment_methods(),
        'brands': ViewServiceUtility.get_all_brands(),
        'categoryData': category_data,
        'breadcrumbs': breadcrumb,
        'store_motivations': ViewServiceUtility.get_store_motivations(),
        'product_count': len(products)
    })
    print(
        f"Rendered template - Total time elapsed: {time.time() - start_time:.4f} seconds")

    return response


@csrf_exempt
def add_to_favorites(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')

        if product_id:
            # Get the user's favorites from the cache
            favorites = cache.get('favorites') or []

            # Toggle product ID in the favorites list
            if product_id in favorites:
                # Remove it if it's already in the list
                favorites.remove(product_id)
            else:
                favorites.append(product_id)  # Add it if it's not in the list

            # Save updated favorites back to the cache
            cache.set('favorites', favorites)

            return JsonResponse({'success': True, 'favorites': favorites})

    return JsonResponse({'success': False}, status=400)


def favorite_products(request, category="Favorieten"):

    # Start timing
    start_time = time.time()

    print(f"Starting 'products_by_category' for category: {category}")

    attributes = request.GET.copy()

    is_sort = ProductSorterUtility.is_sort(attributes)
    is_paginated = ProductSorterUtility.is_paginated(attributes)

    if is_paginated:
        page = attributes.pop('page', None)[0]
        print(f"Pagination value detected: {page}")
    else:
        page = 1

    is_filter = ProductSorterUtility.is_search_filter(attributes)

    if is_sort:
        sort_value = attributes.pop('tn_sort', None)[0]
        print(f"Sort value detected: {sort_value}")

    print(f"Checked sort and pagination flags - Time elapsed: {
          time.time() - start_time:.4f} seconds")

    category_data = {
        "name": "Favorieten",
        "description": "Mijn favorieten producten."
    }
    print(
        f"Retrieved category data - Time elapsed: {time.time() - start_time:.4f} seconds")

    combined_filters = {}

    if is_filter:
        selected_option_filters, selected_slider_filters = ProductSorterUtility.create_filters(
            attributes)
        print(
            f"Created filters - Time elapsed: {time.time() - start_time:.4f} seconds")

        for key, values in selected_option_filters.items():
            combined_filters[key] = list(values)

        for key, values in selected_slider_filters.items():
            combined_filters[key] = list(values)

        products = ProductService.get_filtered_products_by_cache(
            selected_option_filters, selected_slider_filters, cache)
        print(
            f"Filtered products by attributes - Time elapsed: {time.time() - start_time:.4f} seconds")

        if is_sort:
            products = QueryProductSorter.sort_by(products, sort_value)
            print(
                f"Sorted products by attribute - Time elapsed: {time.time() - start_time:.4f} seconds")
        else:
            products = QueryProductSorter.sort_default(products)
            print(f"Applied default sorting to products - Time elapsed: {
                  time.time() - start_time:.4f} seconds")
    else:

        products = ProductService.get_favorite_cached_products(cache)

        print(
            f"Fetched products by category - Time elapsed: {time.time() - start_time:.4f} seconds")

        if is_sort:
            products = QueryProductSorter.sort_by(products, sort_value)
            print(
                f"Sorted products by attribute - Time elapsed: {time.time() - start_time:.4f} seconds")
        else:
            products = QueryProductSorter.sort_default(products)
            print(f"Applied default sorting to products - Time elapsed: {
                  time.time() - start_time:.4f} seconds")

    breadcrumb = [category]
    paginator = Paginator(products, 30)

    try:
        paginated_products = paginator.page(page)
    except PageNotAnInteger:
        paginated_products = paginator.page(1)
    except EmptyPage:
        paginated_products = paginator.page(paginator.num_pages)
    print(
        f"Paginated products - Time elapsed: {time.time() - start_time:.4f} seconds")

    page_obj = paginator.get_page(page)

    filter_data = ProductFilterService.get_products_filters_by_products(
        products, "Assortiment", combined_filters)

    print(
        f"Retrieved filter data - Time elapsed: {time.time() - start_time:.4f} seconds")

    price_filter = ProductFilterService.create_filter_for_price(products)

    if is_filter and price_filter.name not in combined_filters:
        # Only add filters that have more than one value
        if price_filter.lowest != price_filter.highest:
            filter_data.append(price_filter)
    else:
        # Always add values that are already a filter
        if price_filter.lowest != price_filter.highest:
            filter_data.append(price_filter)

    print(
        f"Added price filter - Time elapsed: {time.time() - start_time:.4f} seconds")

    if is_filter:
        filter_data = ProductFilterService.sort_product_filters_on_importance(
            filter_data, combined_filters)
    else:
        filter_data = ProductFilterService.sort_product_filters_on_importance(
            filter_data)
    print(
        f"Sorted product filters - Time elapsed: {time.time() - start_time:.4f} seconds")

    response = render(request, 'products.html', {
        'page_obj': page_obj,
        'products': ViewServiceUtility.get_product_views(paginated_products),
        'filter_data': filter_data,
        'headerData': ViewServiceUtility.get_header_data(),
        'env': environment,
        'store_data': ViewServiceUtility.get_current_store_data(),
        'payment_methods': ViewServiceUtility.get_payment_methods(),
        'brands': ViewServiceUtility.get_all_brands(),
        'categoryData': category_data,
        'breadcrumbs': breadcrumb,
        'store_motivations': ViewServiceUtility.get_store_motivations(),
        'product_count': len(products)
    })
    print(
        f"Rendered template - Total time elapsed: {time.time() - start_time:.4f} seconds")

    return response


def discount_products(request, category='Kortingen'):
    # Start timing
    start_time = time.time()

    print(f"Starting 'products_by_category' for category: {category}")

    attributes = request.GET.copy()

    is_sort = ProductSorterUtility.is_sort(attributes)
    is_paginated = ProductSorterUtility.is_paginated(attributes)

    if is_paginated:
        page = attributes.pop('page', None)[0]
        print(f"Pagination value detected: {page}")
    else:
        page = 1

    is_filter = ProductSorterUtility.is_filter(attributes)

    if is_sort:
        sort_value = attributes.pop('tn_sort', None)[0]
        print(f"Sort value detected: {sort_value}")

    print(f"Checked sort and pagination flags - Time elapsed: {
          time.time() - start_time:.4f} seconds")

    category_data = ProductCategoryService().get_product_category_by_name(category)
    print(
        f"Retrieved category data - Time elapsed: {time.time() - start_time:.4f} seconds")
    combined_filters = {}

    if is_filter:
        selected_option_filters, selected_slider_filters = ProductSorterUtility.create_filters(
            attributes)
        print(
            f"Created filters - Time elapsed: {time.time() - start_time:.4f} seconds")

        for key, values in selected_option_filters.items():
            combined_filters[key] = list(values)

        for key, values in selected_slider_filters.items():
            combined_filters[key] = list(values)

        products = ProductService.get_filtered_products_by_value_and_category(
            selected_option_filters, selected_slider_filters, category)
        print(
            f"Filtered products by attributes - Time elapsed: {time.time() - start_time:.4f} seconds")

        if is_sort:
            products = QueryProductSorter.sort_by(products, sort_value)
            print(
                f"Sorted products by attribute - Time elapsed: {time.time() - start_time:.4f} seconds")
        else:
            products = QueryProductSorter.sort_default(products)
            print(f"Applied default sorting to products - Time elapsed: {
                  time.time() - start_time:.4f} seconds")
    else:

        products = ProductService.get_products_on_sale()

        print(
            f"Fetched products by category - Time elapsed: {time.time() - start_time:.4f} seconds")

        if is_sort:
            products = QueryProductSorter.sort_by(products, sort_value)
            print(
                f"Sorted products by attribute - Time elapsed: {time.time() - start_time:.4f} seconds")
        else:
            products = QueryProductSorter.sort_default(products)
            print(f"Applied default sorting to products - Time elapsed: {
                  time.time() - start_time:.4f} seconds")

    breadcrumb = [category]
    paginator = Paginator(products, 30)

    try:
        paginated_products = paginator.page(page)
    except PageNotAnInteger:
        paginated_products = paginator.page(1)
    except EmptyPage:
        paginated_products = paginator.page(paginator.num_pages)
    print(
        f"Paginated products - Time elapsed: {time.time() - start_time:.4f} seconds")

    page_obj = paginator.get_page(page)

    filter_data = ProductFilterService.get_products_filters_by_products(
        products, "Assortiment", combined_filters)
    print(
        f"Retrieved filter data - Time elapsed: {time.time() - start_time:.4f} seconds")

    if len(filter_data) > 0:

        price_filter = ProductFilterService.create_filter_for_price(products)

        if is_filter and price_filter.name not in combined_filters:
            # Only add filters that have more than one value
            if price_filter.lowest != price_filter.highest:
                filter_data.append(price_filter)
        else:
            # Always add values that are already a filter
            if price_filter.lowest != price_filter.highest:
                filter_data.append(price_filter)

        print(
            f"Added price filter - Time elapsed: {time.time() - start_time:.4f} seconds")

    if is_filter:
        filter_data = ProductFilterService.sort_product_filters_on_importance(
            filter_data, combined_filters)
    else:
        filter_data = ProductFilterService.sort_product_filters_on_importance(
            filter_data)
    print(
        f"Sorted product filters - Time elapsed: {time.time() - start_time:.4f} seconds")

    product_views = ViewServiceUtility.get_product_views(paginated_products)
    print(
        f"Generated product views - Time elapsed: {time.time() - start_time:.4f} seconds")
    response = render(request, 'products.html', {
        'page_obj': page_obj,
        'products': product_views,
        'filter_data': filter_data,
        'headerData': ViewServiceUtility.get_header_data(),
        'env': environment,
        'store_data': ViewServiceUtility.get_current_store_data(),
        'payment_methods': ViewServiceUtility.get_payment_methods(),
        'brands': ViewServiceUtility.get_all_brands(),
        'categoryData': category_data,
        'breadcrumbs': breadcrumb,
        'store_motivations': ViewServiceUtility.get_store_motivations(),
        'product_count': len(products)
    })
    print(
        f"Rendered template - Total time elapsed: {time.time() - start_time:.4f} seconds")

    return response


def runner_products(request, category='Hardlopers'):
    # Start timing
    start_time = time.time()

    print(f"Starting 'products_by_category' for category: {category}")

    attributes = request.GET.copy()

    is_sort = ProductSorterUtility.is_sort(attributes)
    is_paginated = ProductSorterUtility.is_paginated(attributes)

    if is_paginated:
        page = attributes.pop('page', None)[0]
        print(f"Pagination value detected: {page}")
    else:
        page = 1

    is_filter = ProductSorterUtility.is_filter(attributes)

    if is_sort:
        sort_value = attributes.pop('tn_sort', None)[0]
        print(f"Sort value detected: {sort_value}")

    print(f"Checked sort and pagination flags - Time elapsed: {
          time.time() - start_time:.4f} seconds")

    category_data = ProductCategoryService().get_product_category_by_name(category)
    print(
        f"Retrieved category data - Time elapsed: {time.time() - start_time:.4f} seconds")
    combined_filters = {}

    if is_filter:
        selected_option_filters, selected_slider_filters = ProductSorterUtility.create_filters(
            attributes)
        print(
            f"Created filters - Time elapsed: {time.time() - start_time:.4f} seconds")

        for key, values in selected_option_filters.items():
            combined_filters[key] = list(values)

        for key, values in selected_slider_filters.items():
            combined_filters[key] = list(values)

        products = ProductService.get_filtered_products_by_value_and_category(
            selected_option_filters, selected_slider_filters, category)
        print(
            f"Filtered products by attributes - Time elapsed: {time.time() - start_time:.4f} seconds")

        if is_sort:
            products = QueryProductSorter.sort_by(products, sort_value)
            print(
                f"Sorted products by attribute - Time elapsed: {time.time() - start_time:.4f} seconds")
        else:
            products = QueryProductSorter.sort_default(products)
            print(f"Applied default sorting to products - Time elapsed: {
                  time.time() - start_time:.4f} seconds")
    else:

        products = ProductService.get_products_runners()

        print(
            f"Fetched products by category - Time elapsed: {time.time() - start_time:.4f} seconds")

        if is_sort:
            products = QueryProductSorter.sort_by(products, sort_value)
            print(
                f"Sorted products by attribute - Time elapsed: {time.time() - start_time:.4f} seconds")
        else:
            products = QueryProductSorter.sort_default(products)
            print(f"Applied default sorting to products - Time elapsed: {
                  time.time() - start_time:.4f} seconds")

    breadcrumb = [category]
    paginator = Paginator(products, 30)

    try:
        paginated_products = paginator.page(page)
    except PageNotAnInteger:
        paginated_products = paginator.page(1)
    except EmptyPage:
        paginated_products = paginator.page(paginator.num_pages)
    print(
        f"Paginated products - Time elapsed: {time.time() - start_time:.4f} seconds")

    page_obj = paginator.get_page(page)

    filter_data = ProductFilterService.get_products_filters_by_products(
        products, "Assortiment", combined_filters)
    print(
        f"Retrieved filter data - Time elapsed: {time.time() - start_time:.4f} seconds")

    if len(filter_data) > 0:

        price_filter = ProductFilterService.create_filter_for_price(products)

        if is_filter and price_filter.name not in combined_filters:
            # Only add filters that have more than one value
            if price_filter.lowest != price_filter.highest:
                filter_data.append(price_filter)
        else:
            # Always add values that are already a filter
            if price_filter.lowest != price_filter.highest:
                filter_data.append(price_filter)
        print(
            f"Added price filter - Time elapsed: {time.time() - start_time:.4f} seconds")

    if is_filter:
        filter_data = ProductFilterService.sort_product_filters_on_importance(
            filter_data, combined_filters)
    else:
        filter_data = ProductFilterService.sort_product_filters_on_importance(
            filter_data)
    print(
        f"Sorted product filters - Time elapsed: {time.time() - start_time:.4f} seconds")

    product_views = ViewServiceUtility.get_product_views(paginated_products)
    print(
        f"Generated product views - Time elapsed: {time.time() - start_time:.4f} seconds")
    response = render(request, 'products.html', {
        'page_obj': page_obj,
        'products': product_views,
        'filter_data': filter_data,
        'headerData': ViewServiceUtility.get_header_data(),
        'env': environment,
        'store_data': ViewServiceUtility.get_current_store_data(),
        'payment_methods': ViewServiceUtility.get_payment_methods(),
        'brands': ViewServiceUtility.get_all_brands(),
        'categoryData': category_data,
        'breadcrumbs': breadcrumb,
        'store_motivations': ViewServiceUtility.get_store_motivations(),
        'product_count': len(products)
    })
    print(
        f"Rendered template - Total time elapsed: {time.time() - start_time:.4f} seconds")

    return response


def products_by_category(request, category):
    # Start timing
    start_time = time.time()

    print(f"Starting 'products_by_category' for category: {category}")

    attributes = request.GET.copy()

    is_sort = ProductSorterUtility.is_sort(attributes)
    is_paginated = ProductSorterUtility.is_paginated(attributes)

    if is_paginated:
        page = attributes.pop('page', None)[0]
        print(f"Pagination value detected: {page}")
    else:
        page = 1

    is_filter = ProductSorterUtility.is_filter(attributes)

    if is_sort:
        sort_value = attributes.pop('tn_sort', None)[0]
        print(f"Sort value detected: {sort_value}")

    print(f"Checked sort and pagination flags - Time elapsed: {
          time.time() - start_time:.4f} seconds")

    category_data = ProductCategoryService().get_product_category_by_name(category)
    print(
        f"Retrieved category data - Time elapsed: {time.time() - start_time:.4f} seconds")

    if is_filter:
        selected_option_filters, selected_slider_filters = ProductSorterUtility.create_filters(
            attributes)
        print(
            f"Created filters - Time elapsed: {time.time() - start_time:.4f} seconds")

        combined_filters = {}

        for key, values in selected_option_filters.items():
            combined_filters[key] = list(values)

        for key, values in selected_slider_filters.items():
            combined_filters[key] = list(values)

        products = ProductService.get_filtered_products_by_value_and_category(
            selected_option_filters, selected_slider_filters, category)
        print(
            f"Filtered products by attributes - Time elapsed: {time.time() - start_time:.4f} seconds")

        if is_sort:
            products = QueryProductSorter.sort_by(products, sort_value)
            print(
                f"Sorted products by attribute - Time elapsed: {time.time() - start_time:.4f} seconds")
        else:
            products = QueryProductSorter.sort_default(products)
            print(f"Applied default sorting to products - Time elapsed: {
                  time.time() - start_time:.4f} seconds")
    else:

        products = ProductService.get_products_by_attribute(category)

        print(
            f"Fetched products by category - Time elapsed: {time.time() - start_time:.4f} seconds")

        if is_sort:
            products = QueryProductSorter.sort_by(products, sort_value)
            print(
                f"Sorted products by attribute - Time elapsed: {time.time() - start_time:.4f} seconds")
        else:
            products = QueryProductSorter.sort_default(products)
            print(f"Applied default sorting to products - Time elapsed: {
                  time.time() - start_time:.4f} seconds")

    breadcrumb = [category]
    paginator = Paginator(products, 30)

    try:
        paginated_products = paginator.page(page)
    except PageNotAnInteger:
        paginated_products = paginator.page(1)
    except EmptyPage:
        paginated_products = paginator.page(paginator.num_pages)
    print(
        f"Paginated products - Time elapsed: {time.time() - start_time:.4f} seconds")

    page_obj = paginator.get_page(page)

    if is_filter:
        filter_data = ProductFilterService.get_products_filters_by_products(
            products, category, combined_filters)
    else:
        filter_data = ProductFilterService.get_product_filters_by_category(
            category)
    print(
        f"Retrieved filter data - Time elapsed: {time.time() - start_time:.4f} seconds")

    if len(filter_data) > 0:

        price_filter = ProductFilterService.create_filter_for_price(products)

        if is_filter and price_filter.name not in combined_filters:
            # Only add filters that have more than one value
            if price_filter.lowest != price_filter.highest:
                filter_data.append(price_filter)
        else:
            # Always add values that are already a filter
            if price_filter.lowest != price_filter.highest:
                filter_data.append(price_filter)

        print(
            f"Added price filter - Time elapsed: {time.time() - start_time:.4f} seconds")

    if is_filter:
        filter_data = ProductFilterService.sort_product_filters_on_importance(
            filter_data, combined_filters)
    else:
        filter_data = ProductFilterService.sort_product_filters_on_importance(
            filter_data)
    print(
        f"Sorted product filters - Time elapsed: {time.time() - start_time:.4f} seconds")

    product_views = ViewServiceUtility.get_product_views(paginated_products)
    print(
        f"Generated product views - Time elapsed: {time.time() - start_time:.4f} seconds")
    response = render(request, 'products.html', {
        'page_obj': page_obj,
        'products': product_views,
        'filter_data': filter_data,
        'headerData': ViewServiceUtility.get_header_data(),
        'env': environment,
        'store_data': ViewServiceUtility.get_current_store_data(),
        'payment_methods': ViewServiceUtility.get_payment_methods(),
        'brands': ViewServiceUtility.get_all_brands(),
        'categoryData': category_data,
        'breadcrumbs': breadcrumb,
        'store_motivations': ViewServiceUtility.get_store_motivations(),
        'product_count': len(products)
    })
    print(
        f"Rendered template - Total time elapsed: {time.time() - start_time:.4f} seconds")

    return response


def products_by_subcategory(request, category, subcategory):
    # Start timing
    start_time = time.time()

    print(f"Starting 'products_by_category' for category: {category}")

    attributes = request.GET.copy()

    is_sort = ProductSorterUtility.is_sort(attributes)
    is_paginated = ProductSorterUtility.is_paginated(attributes)

    if is_paginated:
        page = attributes.pop('page', None)[0]
        print(f"Pagination value detected: {page}")
    else:
        page = 1

    is_filter = ProductSorterUtility.is_filter(attributes)

    if is_sort:
        sort_value = attributes.pop('tn_sort', None)[0]
        print(f"Sort value detected: {sort_value}")

    print(f"Checked sort and pagination flags - Time elapsed: {
          time.time() - start_time:.4f} seconds")

    category_data = ProductCategoryService().get_product_category_by_name(subcategory)
    print(
        f"Retrieved category data - Time elapsed: {time.time() - start_time:.4f} seconds")

    if is_filter:
        selected_option_filters, selected_slider_filters = ProductSorterUtility.create_filters(
            attributes)
        print(
            f"Created filters - Time elapsed: {time.time() - start_time:.4f} seconds")

        combined_filters = {}

        for key, values in selected_option_filters.items():
            combined_filters[key] = list(values)

        for key, values in selected_slider_filters.items():
            combined_filters[key] = list(values)

        products = ProductService.get_filtered_products_by_value_and_category(
            selected_option_filters, selected_slider_filters, category, subcategory)
        print(
            f"Filtered products by attributes - Time elapsed: {time.time() - start_time:.4f} seconds")

        if is_sort:
            products = QueryProductSorter.sort_by(products, sort_value)
            print(
                f"Sorted products by attribute - Time elapsed: {time.time() - start_time:.4f} seconds")
        else:
            products = QueryProductSorter.sort_default(products)
            print(f"Applied default sorting to products - Time elapsed: {
                  time.time() - start_time:.4f} seconds")
    else:

        products = ProductService.get_products_by_attribute_sub(
            category, subcategory)

        print(
            f"Fetched products by category - Time elapsed: {time.time() - start_time:.4f} seconds")

        if is_sort:
            products = QueryProductSorter.sort_by(products, sort_value)
            print(
                f"Sorted products by attribute - Time elapsed: {time.time() - start_time:.4f} seconds")
        else:
            products = QueryProductSorter.sort_default(products)
            print(f"Applied default sorting to products - Time elapsed: {
                  time.time() - start_time:.4f} seconds")

    breadcrumb = [category, subcategory]
    paginator = Paginator(products, 30)

    try:
        paginated_products = paginator.page(page)
    except PageNotAnInteger:
        paginated_products = paginator.page(1)
    except EmptyPage:
        paginated_products = paginator.page(paginator.num_pages)
    print(
        f"Paginated products - Time elapsed: {time.time() - start_time:.4f} seconds")

    page_obj = paginator.get_page(page)

    if is_filter:
        filter_data = ProductFilterService.get_products_filters_by_products(
            products, category, combined_filters, subcategory)
    else:
        filter_data = ProductFilterService.get_product_filters_by_category_sub(category,
                                                                               subcategory)
    print(
        f"Retrieved filter data - Time elapsed: {time.time() - start_time:.4f} seconds")

    if len(filter_data) > 0:

        price_filter = ProductFilterService.create_filter_for_price(products)

        if is_filter and price_filter.name not in combined_filters:
            # Only add filters that have more than one value
            if price_filter.lowest != price_filter.highest:
                filter_data.append(price_filter)
        else:
            # Always add values that are already a filter
            if price_filter.lowest != price_filter.highest:
                filter_data.append(price_filter)

        print(
            f"Added price filter - Time elapsed: {time.time() - start_time:.4f} seconds")

    if is_filter:
        filter_data = ProductFilterService.sort_product_filters_on_importance(
            filter_data, combined_filters)
    else:
        filter_data = ProductFilterService.sort_product_filters_on_importance(
            filter_data)
    print(
        f"Sorted product filters - Time elapsed: {time.time() - start_time:.4f} seconds")

    product_views = ViewServiceUtility.get_product_views(paginated_products)
    print(
        f"Generated product views - Time elapsed: {time.time() - start_time:.4f} seconds")
    response = render(request, 'products.html', {
        'page_obj': page_obj,
        'products': product_views,
        'filter_data': filter_data,
        'headerData': ViewServiceUtility.get_header_data(),
        'env': environment,
        'store_data': ViewServiceUtility.get_current_store_data(),
        'payment_methods': ViewServiceUtility.get_payment_methods(),
        'brands': ViewServiceUtility.get_all_brands(),
        'categoryData': category_data,
        'breadcrumbs': breadcrumb,
        'store_motivations': ViewServiceUtility.get_store_motivations(),
        'product_count': len(products)
    })
    print(
        f"Rendered template - Total time elapsed: {time.time() - start_time:.4f} seconds")

    return response


def products_by_attribute(request, category, subcategory, attribute):
    # Start timing
    start_time = time.time()

    print(f"Starting 'products_by_category' for category: {category}")

    attributes = request.GET.copy()

    is_sort = ProductSorterUtility.is_sort(attributes)
    is_paginated = ProductSorterUtility.is_paginated(attributes)

    if is_paginated:
        page = attributes.pop('page', None)[0]
        print(f"Pagination value detected: {page}")
    else:
        page = 1

    is_filter = ProductSorterUtility.is_filter(attributes)

    if is_sort:
        sort_value = attributes.pop('tn_sort', None)[0]
        print(f"Sort value detected: {sort_value}")

    print(f"Checked sort and pagination flags - Time elapsed: {
          time.time() - start_time:.4f} seconds")

    category_data = ProductCategoryService().get_product_category_by_name(attribute)
    print(
        f"Retrieved category data - Time elapsed: {time.time() - start_time:.4f} seconds")

    if is_filter:
        selected_option_filters, selected_slider_filters = ProductSorterUtility.create_filters(
            attributes)
        print(
            f"Created filters - Time elapsed: {time.time() - start_time:.4f} seconds")

        combined_filters = {}

        for key, values in selected_option_filters.items():
            combined_filters[key] = list(values)

        for key, values in selected_slider_filters.items():
            combined_filters[key] = list(values)

        products = ProductService.get_filtered_products_by_value_and_category(
            selected_option_filters, selected_slider_filters, category, subcategory, attribute)
        print(
            f"Filtered products by attributes - Time elapsed: {time.time() - start_time:.4f} seconds")

        if is_sort:
            products = QueryProductSorter.sort_by(products, sort_value)
            print(
                f"Sorted products by attribute - Time elapsed: {time.time() - start_time:.4f} seconds")
        else:
            products = QueryProductSorter.sort_default(products)
            print(f"Applied default sorting to products - Time elapsed: {
                  time.time() - start_time:.4f} seconds")
    else:

        products = ProductService.get_products_by_attribute_sub_nested(
            category, subcategory, attribute)

        print(
            f"Fetched products by category - Time elapsed: {time.time() - start_time:.4f} seconds")

        if is_sort:
            products = QueryProductSorter.sort_by(products, sort_value)
            print(
                f"Sorted products by attribute - Time elapsed: {time.time() - start_time:.4f} seconds")
        else:
            products = QueryProductSorter.sort_default(products)
            print(f"Applied default sorting to products - Time elapsed: {
                  time.time() - start_time:.4f} seconds")

    breadcrumb = [category, subcategory, attribute]
    paginator = Paginator(products, 30)

    try:
        paginated_products = paginator.page(page)
    except PageNotAnInteger:
        paginated_products = paginator.page(1)
    except EmptyPage:
        paginated_products = paginator.page(paginator.num_pages)
    print(
        f"Paginated products - Time elapsed: {time.time() - start_time:.4f} seconds")

    page_obj = paginator.get_page(page)

    if is_filter:
        filter_data = ProductFilterService.get_products_filters_by_products(
            products, category, combined_filters, subcategory, attribute)
    else:
        filter_data = ProductFilterService.get_product_filters_by_category_sub_nested(category,
                                                                                      subcategory, attribute)
    print(
        f"Retrieved filter data - Time elapsed: {time.time() - start_time:.4f} seconds")

    if len(filter_data) > 0:

        price_filter = ProductFilterService.create_filter_for_price(products)

        if is_filter and price_filter.name not in combined_filters:
            # Only add filters that have more than one value
            if price_filter.lowest != price_filter.highest:
                filter_data.append(price_filter)
        else:
            # Always add values that are already a filter
            if price_filter.lowest != price_filter.highest:
                filter_data.append(price_filter)

        print(
            f"Added price filter - Time elapsed: {time.time() - start_time:.4f} seconds")

    if is_filter:
        filter_data = ProductFilterService.sort_product_filters_on_importance(
            filter_data, combined_filters)
    else:
        filter_data = ProductFilterService.sort_product_filters_on_importance(
            filter_data)
    print(
        f"Sorted product filters - Time elapsed: {time.time() - start_time:.4f} seconds")

    product_views = ViewServiceUtility.get_product_views(paginated_products)
    print(
        f"Generated product views - Time elapsed: {time.time() - start_time:.4f} seconds")
    response = render(request, 'products.html', {
        'page_obj': page_obj,
        'products': product_views,
        'filter_data': filter_data,
        'headerData': ViewServiceUtility.get_header_data(),
        'env': environment,
        'store_data': ViewServiceUtility.get_current_store_data(),
        'payment_methods': ViewServiceUtility.get_payment_methods(),
        'brands': ViewServiceUtility.get_all_brands(),
        'categoryData': category_data,
        'breadcrumbs': breadcrumb,
        'store_motivations': ViewServiceUtility.get_store_motivations(),
        'product_count': len(products)
    })
    print(
        f"Rendered template - Total time elapsed: {time.time() - start_time:.4f} seconds")

    return response


def product_detail(request, id=None):

    product = ViewServiceUtility.get_product_view_by_id(id)

    if not product:
        return render(request, '404.html')

    product_data = {'product': product,
                    'headerData': ViewServiceUtility.get_header_data(),
                    'env': environment,
                    'store_data': ViewServiceUtility.get_current_store_data(),
                    'payment_methods': ViewServiceUtility.get_payment_methods(),
                    'brands': ViewServiceUtility.get_all_brands(),
                    'alternative_products': ViewServiceUtility.get_alternative_products(id),
                    'store_motivations': ViewServiceUtility.get_store_motivations()}

    if product.product_type == "Vloer":
        misc_products = ViewServiceUtility.get_misc_products()
        product_data['misc_products'] = misc_products

    return render(request, 'product_detail.html', product_data)


def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        pack_quantity = request.POST.get('packs')
        is_product_detail = request.POST.get('is_product_detail')
        print(type(is_product_detail), request.POST)
        try:
            quantity = int(pack_quantity)
        except (TypeError, ValueError):
            quantity = 1

        product = ProductService().get_product_by_id(product_id)

        ShoppingCartService(request).add_item(product.id, quantity)

        if is_product_detail:
            messages.add_message(
                request, messages.SUCCESS, 'Toegevoegd aan je winkelmand.', extra_tags='cart-success')
        else:
            messages.add_message(
                request, messages.SUCCESS, 'Toegevoegd aan je winkelmand.')

    return redirect(request.META.get('HTTP_REFERER', '/'))


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


def get_favorite_count(request):
    favorites = cache.get('favorites') or []

    return JsonResponse({'count': len(favorites)})


def get_shopping_cart(request):
    cart_details = ShoppingCartService(request).to_json()

    return JsonResponse({'cart': cart_details})


def delete_cart_item(request):
    if request.method == 'POST':
        product_id = request.POST.get('id')
        ShoppingCartService(request).remove_item(product_id)
        return redirect('cart')


@csrf_exempt
def mollie_webhook(request):
    print("mollie webhook called")
    if request.method == 'POST':
        try:
            print("POST executing....")
            payment_id = request.POST.get('id')

            payment = MollieClient().get_payment(payment_id)
            payment_id = payment.id
            print("Payment fetched: ", payment, payment_id)
            new_order = OrderService.update_payment_status(
                payment_id, payment.status)
            print("New order in wehook: ", new_order,
                  " with status: ", new_order.order_status)
            if new_order.is_paid:
                AdminMailSender(mail_manager=HTMLMailManager()
                                ).send_order_confirmation(new_order)

                rating_url = url_manager.store_rating()
                account = new_order.account

                if account:
                    salutation = account.salutation
                    last_name = account.last_name
                    email = account.email
                else:
                    salutation = new_order.salutation
                    last_name = new_order.last_name
                    email = new_order.email

                redirect_url = url_manager.create_redirect(new_order.id)

                ClientMailSender(mail_manager=HTMLMailManager()).send_order_payment_confirmation(salutation,
                                                                                                 last_name,
                                                                                                 email,
                                                                                                 new_order.order_number,
                                                                                                 redirect_url)

                ClientMailSender(mail_manager=HTMLMailManager()).send_store_rating(salutation,
                                                                                   last_name,
                                                                                   email,
                                                                                   rating_url)

            return JsonResponse({'status': 'success'})
        except Exception as e:
            print("Error processing Mollie webhook notification:", str(e))
            return JsonResponse({'status': 'error'}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def return_payment_webhook(request):
    if request.method == 'POST':
        try:

            payment_id = request.POST.get('id')

            payment = MollieClient().get_payment(payment_id)
            payment_id = payment.id

            new_order = ReturnService.update_payment_status(
                payment_id, payment.status)

            if new_order.is_paid:
                AdminMailSender(mail_manager=HTMLMailManager()
                                ).send_return_order_confirmation(new_order)

                redirect_url = url_manager.create_redirect_return(new_order.id)

                account = new_order.order.account

                if account:
                    salutation = account.salutation
                    last_name = account.last_name
                    email = account.email
                else:
                    salutation = new_order.order.salutation
                    last_name = new_order.last_name
                    email = new_order.email_address

                ClientMailSender(mail_manager=HTMLMailManager()).send_return_payment_confirmation(salutation,
                                                                                                  last_name,
                                                                                                  email,
                                                                                                  new_order.order.order_number,
                                                                                                  redirect_url)

            return JsonResponse({'status': 'success'})
        except Exception as e:
            print("Error processing Mollie webhook notification:", str(e))
            return JsonResponse({'status': 'error'}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def order_returnable(request):
    if request.method == 'GET':
        order_id = request.GET.get('order_id')
        is_returnable = OrderService.is_order_returnable(order_id)

        return JsonResponse({'is_returnable': is_returnable})


@csrf_exempt
def validate_return_order(request):
    if request.method == "POST":
        data = json.loads(request.body)
        return_products = data.get("returnProducts", {})

        if not return_products:
            return JsonResponse({"success": False, "message": "No products selected. Something went wrong fetching the data..."})

        validation_passed = ValidationService.validate_return_order_lines(
            return_products)

        # If validation passes
        if validation_passed:
            return JsonResponse({"success": True, "message": "Validation passed"})
        else:
            messages.error(
                request, "Het is niet gelukt om een retour aan te maken, check alsjeblieft de ingevulde waarden van de orderregels.")
            return JsonResponse({"success": False, "message": "Validation not passed"})

    return JsonResponse({"success": False, "message": "Invalid request method."})


def create_return(request):
    if request.method == 'GET':
        order_id = request.GET.get('order_id')

        if not order_id:
            return redirect('account')

        is_returnable = OrderService.is_order_returnable(order_id)

        if not is_returnable:
            redirect_url = reverse('order_detail') + f'?order_id={order_id}'

            return redirect(redirect_url)

        return render(request, "return_create.html", {'headerData': ViewServiceUtility.get_header_data(),
                                                      'env': environment,
                                                      'store_data': ViewServiceUtility.get_current_store_data(),
                                                      'payment_methods': ViewServiceUtility.get_payment_methods(),
                                                      'brands': ViewServiceUtility.get_all_brands(),
                                                      'order': ViewServiceUtility.get_order_by_id_for_return(order_id),
                                                      'store_motivations': ViewServiceUtility.get_store_motivations()})
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)

            return_line_data = data.get('returnProducts')
            order_id = data.get('orderId')

            return_order_service = SessionReturnOrderService(request)
            cached_order = return_order_service.add_return_order(
                order_id, return_line_data)

            return JsonResponse({"return_id": cached_order.order_id})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)


def create_return_overview(request):
    if request.method == 'GET':
        return_id = request.GET.get('return_id')

        if not return_id:
            return redirect('account')

        return_order_service = SessionReturnOrderService(request)
        return_order = return_order_service.get_cached_order(return_id)

        account_details = OrderService.get_account_order_details(return_id)

        if "form_data" in return_order:
            initial_data = return_order["form_data"]

        else:
            # Prefill form data from account details
            initial_data = {
                'return_reason': '',
                'first_name': account_details.first_name,
                'last_name': account_details.last_name,
                'email_address': account_details.email,
                'address': account_details.address,
                'house_number': account_details.house_number,
                'city': account_details.city,
                'postal_code': account_details.postal_code,
                'country': account_details.country,
                'phone': account_details.phone,
            }

        form = ReturnForm(initial=initial_data)

        return render(
            request,
            "return_create_detail.html",
            {
                'headerData': ViewServiceUtility.get_header_data(),
                'env': environment,
                'return_order': return_order,
                'store_data': ViewServiceUtility.get_current_store_data(),
                'payment_methods': ViewServiceUtility.get_payment_methods(),
                'brands': ViewServiceUtility.get_all_brands(),
                'store_motivations': ViewServiceUtility.get_store_motivations(),
                'form': form,
            },
        )
    elif request.method == 'POST':
        # Retrieve return_id from POST data
        return_id = request.POST.get('return_id')

        if not return_id:
            return redirect('account')

        return_order_service = SessionReturnOrderService(request)
        return_order = return_order_service.get_cached_order(return_id)

        # Bind POST data to the form
        form = ReturnForm(request.POST)

        if form.is_valid():

            is_returnable = OrderService.is_order_returnable(
                return_order["order_id"])

            if not is_returnable:
                # General error
                form.add_error(
                    None, "De gekozen orderrregels zijn aangepast en niet te retourneren.")
                render(request, 'return_create_detail.html',
                       {
                           'form': form,
                           'headerData': ViewServiceUtility.get_header_data(),
                           'env': environment,
                           'return_order': return_order,
                           'store_data': ViewServiceUtility.get_current_store_data(),
                           'payment_methods': ViewServiceUtility.get_payment_methods(),
                           'brands': ViewServiceUtility.get_all_brands(),
                           'store_motivations': ViewServiceUtility.get_store_motivations(),
                       })

            result = return_order_service.update_form_data(
                return_id, form.cleaned_data)

            if not result:
                # General error
                form.add_error(
                    None, "Er is iets misgegaan bij het aanmaken van de retour. Probeer het opnieuw")
                render(request, 'return_create_detail.html',
                       {
                           'form': form,
                           'headerData': ViewServiceUtility.get_header_data(),
                           'env': environment,
                           'return_order': return_order,
                           'store_data': ViewServiceUtility.get_current_store_data(),
                           'payment_methods': ViewServiceUtility.get_payment_methods(),
                           'brands': ViewServiceUtility.get_all_brands(),
                           'store_motivations': ViewServiceUtility.get_store_motivations(),
                       })
            else:

                redirect_url = reverse('confirm_return') + \
                    f'?return_id={return_id}'
                return redirect(redirect_url)

        else:
            # If the form is invalid, re-render the page with error messages
            return render(
                request,
                'return_create_detail.html',
                {
                    'form': form,
                    'headerData': ViewServiceUtility.get_header_data(),
                    'env': environment,
                    'return_order': return_order,
                    'store_data': ViewServiceUtility.get_current_store_data(),
                    'payment_methods': ViewServiceUtility.get_payment_methods(),
                    'brands': ViewServiceUtility.get_all_brands(),
                    'store_motivations': ViewServiceUtility.get_store_motivations(),
                },
            )


def confirm_return(request):
    if request.method == 'GET':
        return_id = request.GET.get('return_id')

        if not return_id:
            return redirect('account')

        return_order_service = SessionReturnOrderService(request)
        return_order = return_order_service.get_cached_order(return_id)

        if not return_order:
            return redirect('account')

        if not "form_data" in return_order:
            redirect_url = reverse('create_return_overview') + \
                f'?return_id={return_id}'
            return redirect(redirect_url)

        return render(request, 'return_payment.html',
                      {
                          'headerData': ViewServiceUtility.get_header_data(),
                          'env': environment,
                          'return_order': return_order,
                          'store_data': ViewServiceUtility.get_current_store_data(),
                          'payment_methods': ViewServiceUtility.get_payment_methods(),
                          'brands': ViewServiceUtility.get_all_brands(),
                          'store_motivations': ViewServiceUtility.get_store_motivations(),
                          'payment_issuers': MollieClient().get_issuers('ideal'),
                          'delivery_methods': ViewServiceUtility.get_active_takeaway_methods(),
                      })

    elif request.method == 'POST':

        return_id = request.POST.get('return_id')
        if not return_id:
            return redirect('account')
        issuer_id = request.POST.get('issuer_id')
        issuer_name = request.POST.get('issuer_name')
        payment_method = request.POST.get('payment_method')
        payment_name = request.POST.get('payment_name')
        delivery_method = request.POST.get('selected_delivery_method')
        delivery_date = request.POST.get('delivery_date')

        payment_info = PaymentInfo(
            payment_name, issuer_name, issuer_id, payment_method)
        delivery_info = DeliveryInfo(delivery_method, delivery_date)

        return_order_service = SessionReturnOrderService(request)
        return_order = return_order_service.get_cached_order(return_id)

        if not return_order:
            return redirect('account')

        created_return_order = ReturnService.create_return_order_with_lines(
            return_order, return_order['form_data'], payment_info, delivery_info)

        if not created_return_order:

            return render(request, 'return_payment.html',
                          {
                              'headerData': ViewServiceUtility.get_header_data(),
                              'env': environment,
                              'return_order': return_order,
                              'store_data': ViewServiceUtility.get_current_store_data(),
                              'payment_methods': ViewServiceUtility.get_payment_methods(),
                              'brands': ViewServiceUtility.get_all_brands(),
                              'store_motivations': ViewServiceUtility.get_store_motivations(),
                          })

        redirect_url = url_manager.create_redirect_return(
            created_return_order.id)
        webhook_url = url_manager.create_return_webhook()

        # Remove order from cache
        return_order_service = SessionReturnOrderService(request)
        return_order_service.clear_order(
            return_order["order_id"])

        print(payment_method, issuer_id, issuer_name, payment_name)
        payment = MollieClient().create_payment('EUR', str(
            created_return_order.refund_amount), created_return_order.order.order_number, redirect_url, webhook_url, payment_method, issuer_id)

        ReturnService.add_payment(payment, created_return_order.id)

        checkout_url = payment['_links']['checkout']['href']
        print(payment, checkout_url)

        account = request.user
        order = created_return_order

        if account.is_authenticated:
            salutation = account.salutation
            last_name = account.last_name
            email = account.email
        else:
            salutation = order.order.salutation
            last_name = order.last_name
            email = order.email_address

        ClientMailSender(mail_manager=HTMLMailManager()).send_return_confirmation(salutation,
                                                                                  last_name,
                                                                                  email,
                                                                                  created_return_order.order.order_number,
                                                                                  redirect_url)

        return redirect(checkout_url)


def return_detail(request):
    if request.method == 'GET':
        return_id = request.GET.get('return_id')

        if not return_id:
            return redirect('account')

        return_order = ViewServiceUtility.get_return_order_by_id(return_id)
        progress_phases = get_order_progress_phases(return_order.status)

        return render(request, "return_detail.html", {'headerData': ViewServiceUtility.get_header_data(),
                                                      'env': environment,
                                                      'store_data': ViewServiceUtility.get_current_store_data(),
                                                      'payment_methods': ViewServiceUtility.get_payment_methods(),
                                                      'brands': ViewServiceUtility.get_all_brands(),
                                                      'order': return_order,
                                                      'progress_phases': progress_phases,
                                                      'store_motivations': ViewServiceUtility.get_store_motivations()})
