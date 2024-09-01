
from ecommerce_website.models import Order, StoreRating


class AccountService:

    @staticmethod
    def can_write_review(account_id) -> bool:

        order_count = Order.objects.filter(account_id=account_id).count()
        review_count = StoreRating.objects.filter(
            user_id=account_id).count()

        return order_count > 0 and order_count != review_count
