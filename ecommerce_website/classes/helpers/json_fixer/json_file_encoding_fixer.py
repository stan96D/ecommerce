import json


class JSONEncodingFixer:
    def __init__(self, file_path):
        self.file_path = file_path

    def decode_text(self, binary_data, encodings=['utf-8', 'latin-1']):
        for encoding in encodings:
            try:
                return binary_data.decode(encoding)
            except UnicodeDecodeError:
                continue
        # If all encodings fail, return the data with errors replaced
        return binary_data.decode('utf-8', errors='replace')

    def fix_encoding(self, text):
        try:
            # Decode from 'latin-1' to 'utf-8'
            return text.encode('latin-1').decode('utf-8')
        except (UnicodeEncodeError, UnicodeDecodeError):
            # Return the original text if decoding fails
            return text

    def fix_json_encoding(self, data):
        if isinstance(data, dict):
            return {self.fix_encoding(k): self.fix_json_encoding(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.fix_json_encoding(item) for item in data]
        elif isinstance(data, str):
            return self.fix_encoding(data)
        else:
            return data

    def update_file(self):
        # Read the JSON file in binary mode
        with open(self.file_path, 'rb') as file:
            binary_data = file.read()

        # Decode the binary data using a list of encodings
        decoded_data = self.decode_text(binary_data)

        # Load JSON data from the decoded text
        try:
            data = json.loads(decoded_data)
        except json.JSONDecodeError:
            print(
                "Failed to decode JSON. The file might be corrupt or not properly formatted.")
            return

        # Fix encoding issues in the JSON data
        fixed_data = self.fix_json_encoding(data)

        # Write the corrected data back to the file with UTF-8 encoding
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(fixed_data, file, ensure_ascii=False, indent=4)

        print(f"File '{self.file_path}' has been updated with fixed encoding.")


# Example usage
# Using raw string for Windows path
file_path = r'ecommerce_website\db_mapper\data\finalized_minimal.json'
fixer = JSONEncodingFixer(file_path)
fixer.update_file()
