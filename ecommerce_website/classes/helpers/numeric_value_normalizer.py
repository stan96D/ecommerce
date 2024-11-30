
import re


def extract_value_and_unit(value_str):
    """
        Extract the numeric value and the unit from the input string.
        Returns a tuple (numeric_value_as_string, unit).
        """

    match = re.search(
        r"([-+]?\d*\.\d+|\d+)(\s*(mm|cm|m|m2|€)?)", value_str)
    if match:
        numeric_value = match.group(1)  # Keep numeric part as string
        unit = match.group(3).strip() if match.group(
            3) else None  # Extract unit, if present
        return numeric_value, unit
    else:
        return None, None  # Return "0" and empty unit if no match found


def is_value_in_range(value_str, range_values):
    try:
        # Convert the string to a float
        value = float(value_str)

        # Check if the value is within the range (inclusive)
        lowest, highest = range_values
        if lowest <= value <= highest:
            return True
        else:
            return False
    except ValueError:
        # Handle the case where the string cannot be converted to a float
        print(f"Invalid value: {value_str} cannot be converted to a float.")
        return False


def extract_lowest_and_highest(values):
    """
    Extract the lowest and highest values from a list of integers.
    If no distinct lowest value exists (due to duplicates or a single value), return 0 for the lowest.

    :param values: List of integers
    :return: List of two integers [lowest, highest]
    """
    if not values:
        return [0, 0]  # Return [0, 0] for an empty list

    unique_values = list(set(values))  # Remove duplicates
    if len(unique_values) < 2:
        # If there is only one unique value, return 0 as the lowest
        return [0, unique_values[0]]

    # Sort unique values to find the lowest and highest
    unique_values.sort()
    return [unique_values[0], unique_values[-1]]
