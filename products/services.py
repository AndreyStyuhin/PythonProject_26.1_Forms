# products/services.py
from .models import Product

def get_products_by_category(category_name: str):
    return Product.objects.filter(category=category_name, status="published")
