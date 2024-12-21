import json


def update_prices_in_json(file_path, multiplier):
    """
    Update the 'Prijs per m2' and 'Prijs per pak' in a JSON file by a given multiplier,
    but only for products where 'Leverancier' is 'Peitsman'.

    :param file_path: Path to the JSON file
    :param multiplier: Multiplier to adjust the prices
    :return: None (updates the JSON file directly)
    """
    try:
        # Read the data from the JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            products = json.load(file)

        # Loop over each product in the list
        updated_count = 0
        for product in products:
            # Check if 'Leverancier' is 'Peitsman'
            if 'Leverancier' in product and product['Leverancier'] == 'Peitsman':
                # Update 'Prijs per m2' and 'Prijs per pak' by applying the multiplier
                if 'Prijs per m²' in product:
                    product['Prijs per m²'] = round(
                        product['Prijs per m²'] * multiplier, 2)
                if 'Prijs per pak' in product:
                    product['Prijs per pak'] = round(
                        product['Prijs per pak'] * multiplier, 2)

                updated_count += 1

        # Write the updated products back to the JSON file
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(products, file, ensure_ascii=False, indent=4)

        print(f"Prices updated for {
              updated_count} products and saved to {file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")
