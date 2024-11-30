from decimal import Decimal


class WebShopConfig:

    @staticmethod
    def excluded_filters():
        return [
            "Afmeting",
            "Type",
            "SKU",
            "Producttype",
            "Omschrijving",
            "Leverancier",
            "Weekmakervrij",
            "Garantie commercieel",
            "Beschikbaarheid",
            "Kant-en-klaar",
            "Garantie huishoudelijk",
            "Links",
            "Garantie periode",
            "Eenheid",
            "Overlap",
            "Oppervlakte",
            "Pakinhoud",
            "Productcode van de fabrikant"
        ]

    @staticmethod
    def slider_filters():
        return [
            "Dikte",
            "Lengte",
            "Breedte",
            "Toplaagdikte",
            "Dikte toplaag",
            "Warmteweerstand (m²K/W)",
            "Dikte onderlaag",
            "Dikte tussenlaag",
            "Slijtlaag",

        ]

    @staticmethod
    def search_filters():
        return [
            "Vloertype",
            "Type",
            "Merk",
            "Model",
            "Kleur",
            "Collectie",
        ]

    @staticmethod
    def shipping_margin():
        return Decimal('1.05')

    @staticmethod
    def return_days():
        return 14

    @staticmethod
    def contact_email():
        return "info@goedkoopstevloerenshop.com"

    @staticmethod
    def address():
        return ""

    @staticmethod
    def postal_code():
        return ""

    @staticmethod
    def coc_number():
        return ""

    @staticmethod
    def vat_number():
        return ""

    @staticmethod
    def opening_time_week():
        return "10:00-17:00"

    @staticmethod
    def opening_time_weekend():
        return "Gesloten"
