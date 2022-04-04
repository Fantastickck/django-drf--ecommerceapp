from django.urls import path

from .views import get_categories, get_category, get_product, get_brands, get_brand


urlpatterns = [
    path('', get_categories, name='get_categories'),
    path('category/<slug:slug>/', get_category, name='get_category'),
    path('product/<int:product_id>/', get_product, name='get_product'),
    path('brands/', get_brands, name='get_brands'),
    path('brand/<slug:slug>/', get_brand, name='get_brand'),
]