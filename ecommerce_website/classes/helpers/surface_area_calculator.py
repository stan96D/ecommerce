import math
import re

class SurfaceAreaCalculator:
    @staticmethod
    def parse_surface_area(surface):
        if isinstance(surface, str):
            match = re.search(r'[\d\.]+', surface)
            if match:
                return float(match.group())
            else:
                raise ValueError(f"Invalid surface area format: {surface}")
        elif isinstance(surface, (int, float)):
            return float(surface)
        else:
            raise TypeError(
                f"Unsupported type for surface area: {type(surface)}")

    @staticmethod
    def calculate_floors_per_package(pack_content, floor_surface):

        pack_content = SurfaceAreaCalculator.parse_surface_area(pack_content)
        floor_surface = SurfaceAreaCalculator.parse_surface_area(floor_surface)

        if floor_surface <= 0:
            raise ValueError(
                "The surface area of one floor must be greater than zero.")

        floors_per_package = pack_content / floor_surface

        return math.ceil(floors_per_package)
