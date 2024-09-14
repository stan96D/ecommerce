import json
import re


class JSONPropertyFormatter:
    def __init__(self, file_path):
        self.file_path = file_path

    def format_property(self, key, value):
        # Regular expression to match keys with units in parentheses
        match = re.match(r"(.+?) \((cm|mm)\)", key)
        if match:
            new_key = match.group(1)
            unit = match.group(2)
            new_value = f"{value} {unit}"
            return new_key, new_value
        return key, value

    def process_data(self, data):
        if isinstance(data, dict):
            formatted_dict = {}
            for k, v in data.items():
                new_key, new_value = self.format_property(k, v)
                formatted_dict[new_key] = self.process_data(new_value)
            return formatted_dict
        elif isinstance(data, list):
            return [self.process_data(item) for item in data]
        else:
            return data

    def update_file(self):
        try:
            # Read the JSON file
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            # Process the data to format properties and values
            formatted_data = self.process_data(data)

            # Write the corrected data back to the file
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(formatted_data, file, ensure_ascii=False, indent=4)

            print(
                f"File '{self.file_path}' has been updated with formatted properties.")

        except Exception as e:
            print(f"An error occurred: {e}")


# Example usage
# Using raw string for Windows path
file_path = r'ecommerce_website\db_mapper\data\final_data\finalized_combined.json'
formatter = JSONPropertyFormatter(file_path)
formatter.update_file()
