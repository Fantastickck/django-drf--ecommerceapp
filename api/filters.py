from django_filters import rest_framework as filters

from catalog.models import Product, Category


class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter()
    price = filters.RangeFilter()
    brand = CharInFilter(field_name='brand__name', lookup_expr='in')

    class Meta:
        model = Product
        fields = ('name', 'price', 'brand', 'category', 'total_rating')


# Незавершенная реализация филтров для товаров определенной категории
class ProductByCategoryFilter(filters.FilterSet):
    products = filters.CharFilter(field_name='products__name')
    price = filters.RangeFilter(field_name='products__price')
    brand = CharInFilter(field_name='products__brand__name', lookup_expr='in')

    class Meta:
        model = Category
        fields = ('products',)
