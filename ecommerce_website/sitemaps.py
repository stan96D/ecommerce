from .models import ProductCategory
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import ProductCategory, Product, ProductFilter, ProductAttribute, ProductStock

# Product Category Sitemap


class ProductCategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        # Only active categories
        return ProductCategory.objects.all()

    def location(self, obj):
        # Dynamically generate the URL for each category
        return reverse('products_by_category', args=[obj.name])


# Product Sitemap


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Product.objects.all()

    def location(self, obj):
        # Assumes you have a URL pattern for product detail pages using `sku`
        return reverse('product_detail', args=[obj.id])

# Product Filter Sitemap (Optional - Only if you want filter pages in the sitemap)


class ProductCategorySitemap(Sitemap):
    def items(self):
        # Fetch all active product categories
        return ProductCategory.objects.filter(active=True)

    def location(self, obj):
        # Dynamically generate the URL for each category
        return reverse('products_by_category', args=[obj.name])

    def changefreq(self, obj):
        return "weekly"  # Adjust frequency based on your content updates

    def priority(self, obj):
        return 0.7  # You can adjust the priority for categories based on your needs


class ProductSubcategorySitemap(Sitemap):
    def items(self):
        # Fetch all subcategories that have products
        return ProductCategory.objects.filter(parent_category__isnull=False)

    def location(self, obj):
        # Generate the URL for each subcategory
        return reverse('products_by_subcategory', args=[obj.parent_category.name, obj.name])

    def changefreq(self, obj):
        return "weekly"  # Adjust frequency based on your content updates

    def priority(self, obj):
        return 0.6  # Lower priority for subcategories compared to main categories



