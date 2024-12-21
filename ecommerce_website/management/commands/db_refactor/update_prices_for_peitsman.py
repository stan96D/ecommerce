from ecommerce_website.models import Product
from decimal import Decimal


def update_prices_for_peitsman(price_multiplier=Decimal('0.475')):

    # Fetch products with specific conditions
    products_to_update = Product.objects.filter(
        attributes__attribute_type__name="Leverancier",
        attributes__value="Peitsman"
    ).distinct()

    print(f'Found {products_to_update.count()} products to update.')

    # Loop through each product and update the price and unit_price
    updated_count = 0
    for product in products_to_update:
        # Update the price
        old_price = product.price
        old_unit_price = product.unit_price
        new_price = old_price * price_multiplier
        new_unit_price = old_unit_price * price_multiplier

        # Save the new prices
        product.price = new_price
        product.unit_price = new_unit_price
        product.save()

        updated_count += 1

        # Print update info
        print(f'Updated product {product.id}: '
              f'Old Price = {old_price}, New Price = {new_price}, '
              f'Old Unit Price = {old_unit_price}, New Unit Price = {new_unit_price}')

    print(f'{updated_count} products were successfully updated.')
