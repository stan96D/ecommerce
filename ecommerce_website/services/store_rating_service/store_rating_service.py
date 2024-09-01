from django.db.models import Avg, Count, Sum
from ecommerce_website.models import StoreRating


class StoreRatingService:
    @staticmethod
    def get_mean():
        """
        Calculate the mean of all the store ratings and return both the original
        and the rounded mean rating (to 2 decimal places).

        :return: A tuple containing the original mean rating and the rounded mean rating.
        """
        mean_rating = StoreRating.objects.aggregate(
            average=Avg('stars'))['average']

        # Round mean rating to 2 decimal places
        rounded_mean_rating = round(
            mean_rating, 2) if mean_rating is not None else 0.0

        return rounded_mean_rating

    @staticmethod
    def get_last(limit=4, min_rating=0):
        """
        Get the last few store ratings with an optional filter on the minimum rating.

        :param limit: The number of ratings to retrieve.
        :param min_rating: The minimum rating to filter on.
        :return: Queryset of the last few ratings.
        """

        return StoreRating.objects.filter(stars__gte=min_rating).order_by('-created_at')[:limit]

    @staticmethod
    def get_count():
        """Get the total count of all store ratings."""
        return StoreRating.objects.count()

    @staticmethod
    def get_star_count():
        """
        Get the count and percentage of ratings grouped by the number of stars.
        :return: A dictionary with star counts and percentages.
        """
        # Get the counts of ratings grouped by the number of stars
        star_counts = StoreRating.objects.values('stars').annotate(
            count=Count('stars')).order_by('stars')

        # Calculate the total number of ratings
        total_ratings = StoreRating.objects.count()

        # Create a dictionary with default values for all stars (0-5)
        star_distribution = {i: {'count': 0, 'percentage': 0}
                             for i in range(6)}

        # Update the dictionary with actual counts and calculate percentages
        for entry in star_counts:
            star = entry['stars']
            count = entry['count']
            percentage = (count / total_ratings *
                          100) if total_ratings > 0 else 0
            star_distribution[star] = {'count': count,
                                       'percentage': round(percentage, 2)}

        # Sort the dictionary by keys in descending order
        sorted_star_distribution = dict(
            sorted(star_distribution.items(), key=lambda item: item[0], reverse=True))

        return sorted_star_distribution
