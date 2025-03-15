from datetime import timedelta
from django.utils.timezone import now
# Update 'myapp' with your actual app name
from ecommerce_website.models import *


def create_opening_sale():
    # Define sale details
    sale_name = "Openingskorting"
    description = "Om onze opening te vieren met jullie, bieden wij jullie allemaal 5% korting aan. Leggen die vloeren!"
    start_date = now().date()
    end_date = start_date + timedelta(days=30)
    discount_percentage = 5  # 5% discount

    # Create sale if it doesn't exist
    sale, created = Sale.objects.get_or_create(
        name=sale_name,
        defaults={
            "active": True,
            "description": description,
            "begin_date": start_date,
            "end_date": end_date,
        },
    )

    if not created:
        print(f"Sale '{sale_name}' already exists.")
    else:
        print(f"Created sale: {sale_name}")

    # Apply sale to all products
    products = Product.objects.all()
    for product in products:
        product_sale, sale_created = ProductSale.objects.get_or_create(
            sale=sale, product=product,
            defaults={"percentage": discount_percentage}
        )
        if sale_created:
            print(
                f"Applied {discount_percentage}% discount to: {product.name}")
        else:
            print(f"Product '{product.name}' already has a sale.")
