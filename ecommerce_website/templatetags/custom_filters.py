# ecommerce_website/templatetags/custom_filters.py

from decimal import Decimal
from django import template
import math

register = template.Library()


@register.filter(name='ceil')
def ceil(value):
    try:
        # Convert the value to a float
        float_value = float(value)

        if float_value < 1:
            # Round up to two decimal places for values < 1
            return math.ceil(float_value * 100) / 100
        elif float_value < 10:
            # Round up to one decimal place for values >= 1 and < 10
            return math.ceil(float_value * 10) / 10
        else:
            # Round up to nearest integer for values >= 10
            return math.ceil(float_value)

    except (ValueError, TypeError):
        return value  # Return the original value if it's not a valid number


@register.filter(name='floor')
def floor(value):
    try:
        # Convert the value to a float
        float_value = float(value)

        if float_value < 1:
            # Round down to two decimal places for values < 1
            return math.floor(float_value * 100) / 100
        elif float_value < 10:
            # Round down to one decimal place for values >= 1 and < 10
            return math.floor(float_value * 10) / 10
        else:
            # Round down to nearest integer for values >= 10
            return math.floor(float_value)

    except (ValueError, TypeError):
        return value  # Return the original value if it's not a valid number


@register.filter(name='calculate_step')
def calculate_step(lowest, highest):
    try:
        # Ensure the values are numeric (floats)
        lowest = floor(float(lowest))
        highest = ceil(float(highest))

        # Calculate the range difference
        range_diff = highest - lowest

        decimal_count = count_decimal_places(range_diff)

        if decimal_count == 2:
            last_digit = range_diff % 0.1
        elif decimal_count == 1:
            last_digit = range_diff % 1
        else:
            if range_diff < 1:
                last_digit = range_diff % 0.1
                if last_digit == 0:
                    last_digit = 0.01

            elif range_diff < 10:
                last_digit = range_diff % 1
                if last_digit == 0:
                    last_digit = 0.1
            elif range_diff < 100:
                last_digit = range_diff % 10
                if last_digit == 0:
                    last_digit = 1
            elif range_diff < 1000:
                last_digit = range_diff % 100
                if last_digit == 0:
                    last_digit = 10
            elif range_diff < 10000:
                last_digit = range_diff % 1000
                if last_digit == 0:
                    last_digit = 100
            elif range_diff < 100000:
                last_digit = range_diff % 10000
                if last_digit == 0:
                    last_digit = 1000

        if last_digit < 0.1:
            return 0.01
        elif last_digit < 1:
            return 0.1
        elif last_digit < 10:
            return 1
        elif last_digit < 100:
            return 10
        elif last_digit < 1000:
            return 100
        elif last_digit < 10000:
            return 1000
        elif last_digit < 10000:
            return 1000

    except (ValueError, TypeError):
        return 1  # Default step if values are invalid


def count_decimal_places(number):
    try:
        # Convert to Decimal for precision
        decimal_number = Decimal(str(number))
        # Get the fractional part by splitting at the decimal point
        fractional_part = decimal_number.as_tuple().exponent
        return abs(fractional_part) if fractional_part < 0 else 0
    except (ValueError, TypeError):
        return 0  # Return 0 if the input isn't valid
