import json
from typing import List, Dict


def modify_json_file(file_path: str, new_property: str, value):
    """
    Reads JSON data from a file, adds a new property with a specified value to each JSON object,
    and writes the updated JSON data back to the same file.

    :param file_path: Path to the JSON file.
    :param new_property: The name of the property to add.
    :param value: The value to set for the new property.
    """
    # Read JSON data from the file
    with open(file_path, 'r') as file:
        json_objects = json.load(file)

    # Add the new property to each JSON object
    for obj in json_objects:
        obj[new_property] = value

    # Write the updated JSON data back to the file
    with open(file_path, 'w') as file:
        json.dump(json_objects, file, indent=2)
