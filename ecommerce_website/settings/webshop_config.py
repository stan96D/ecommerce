from decimal import Decimal

class WebShopConfig:

    @staticmethod
    def shipping_margin():
        return Decimal('1.05')
    
    @staticmethod
    def return_days():
        return 14
    


