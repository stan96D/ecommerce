import requests
from django.http import JsonResponse


class AddressManager:

    # Base API URL and headers can be reused
    BASE_API_URL = "https://nominatim.openstreetmap.org/search"
    HEADERS = {
        "User-Agent": "GoedkoopsteVloerenShop.nl/1.0 (info@goedkoopstevloerenshop.nl)",
    }

    @staticmethod
    def fetch_data_from_api(query):
        """
        Fetches data from the Nominatim API using the given query string.
        Returns the response from the API.
        """
        # Construct the Nominatim API URL with the query parameter
        api_url = f"{AddressManager.BASE_API_URL}?q={query}&format=json&addressdetails=1"

        # Send request to the Nominatim API
        try:
            response = requests.get(api_url, headers=AddressManager.HEADERS)
            response.raise_for_status()  # Will raise HTTPError for bad responses
            return response.json()  # Return JSON response
        except requests.RequestException as e:
            return {"error": str(e)}  # Return error message

    @staticmethod
    def extract_address_data(address_data):
        """
        Extracts relevant address fields from the API response.
        Returns a dictionary with address details.
        """
        address = address_data.get('address', {})
        return {
            'street': address.get('road'),
            'city': address.get('city'),
            # Default to 'Nederland' if no country
            'country': address.get('country', 'Nederland'),
            'postal_code': address.get('postcode'),
        }

    @staticmethod
    def validate_address_data(address_data):
        """
        Validates the address data to ensure it contains the necessary fields.
        Returns True if valid, else False with an error message.
        """
        required_fields = ['street', 'city', 'country', 'postal_code']

        for field in required_fields:
            if not address_data.get(field):
                return False, f"Missing required field: {field}"

        # Additional validation for house number can be added here if needed
        return True, None

    @staticmethod
    def build_query(street, postal_code, house_number, city=None, country=None):
        """
        Builds a query string for the Nominatim API.
        If city and country are provided, they are included in the query.
        """
        query = f"{street} {house_number} {postal_code}"
        if city:
            query += f" {city}"
        if country:
            query += f" {country}"
        return query

    @staticmethod
    def fetch_and_validate_address(street, postal_code, house_number, city=None, country=None):
        """
        Fetches the address data from the Nominatim API, validates the address, and returns a result.
        """
        # Build the query
        query = AddressManager.build_query(
            street, postal_code, house_number, city, country)

        # Fetch data from API
        data = AddressManager.fetch_data_from_api(query)

        # Handle any API errors
        if "error" in data:
            return False  # Return False if there was an API error

        # If no data is returned or the data is empty, return False
        if not data or len(data) == 0:
            return False

        # Extract relevant address data from the response
        address_data = AddressManager.extract_address_data(data[0])

        # Validate the extracted address data
        is_valid, error_message = AddressManager.validate_address_data(
            address_data)

        # Optionally, you can log or print the error message here if necessary
        print(error_message)

        return is_valid
