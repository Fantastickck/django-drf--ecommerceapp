from django.urls import path

from .views import get_categories, get_products, get_product, get_brands, get_categories_by_brand


urlpatterns = [
    path('', get_categories, name='get_categories'),
    path('category/<slug:slug>/', get_products, name='get_products'),
    path('product/<int:product_id>/', get_product, name='get_product'),
    path('brands/', get_brands, name='get_brands'),
    path('brand/<slug:slug>/', get_categories_by_brand, name='get_brand'),
]