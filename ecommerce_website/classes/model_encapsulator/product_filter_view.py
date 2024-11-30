class ProductFilterView:
    def __init__(self, data):
        self.name = data['name']
        self.type = data['filter_type']

        if self.type == 'slider':
            lowest, highest = self.convert_values_to_numbers(
                data['values'])
            self.lowest = lowest
            self.highest = highest
            self.unit = data['unit'] if data['unit'] is not None else ''
        else:
            self.values = data['values']

    def convert_values_to_numbers(self, values):
        # Convert all values to float if they are strings
        numeric_values = []
        for value in values:
            try:
                # Try to convert to float
                numeric_values.append(float(value))
            except ValueError:
                # If value can't be converted, print or handle the error
                print(f"Warning: Unable to convert '{value}' to float.")
                # You can append 0 or handle the error differently
                numeric_values.append(0)

        # Now, find the lowest and highest values
        lowest = min(numeric_values)
        highest = max(numeric_values)

        return lowest, highest
