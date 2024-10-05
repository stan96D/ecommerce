from decimal import Decimal


class WebShopConfig:

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
