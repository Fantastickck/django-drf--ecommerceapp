import django_filters

from .models import Category, Product, Brand


class ProductFilter(django_filters.FilterSet):

    CHOICES = (
        ('ascending_price', 'По возрастанию цены'),
        ('descending_price', 'По убыванию цены'),
        ('descending_order', 'По популярности'),
        ('ascending_rating', 'По возрастанию рейтинга'),
        ('descending_rating', 'По убыванию рейтинга'),
    )

    CHOICES_PRICE = (
        ('10000', '10000 Руб и меньше'),
        ('10001-30000', '10001 - 30000 Руб'),
        ('30001-50000', '30001 - 50000 Руб'),
        ('50001-70000', '50001 - 70000 Руб'),
        ('70001', '70001 Руб и больше')
    )

    ordering = django_filters.ChoiceFilter(
        label='Сортировка', choices=CHOICES, method='order_by')
    # brand_ = django_filters.ModelChoiceFilter(label='Бренд', queryset=Brand.objects.filter())
    price = django_filters.ChoiceFilter(
        label='Цена', choices=CHOICES_PRICE, method='filter_by_price')

    class Meta:
        model = Product
        fields = [
            'brand',
            
        ]

    def order_by(self, queryset, name, value):
        if value == 'ascending_price':
            expression = 'price'
        elif value == 'descending_price':
            expression = '-price'
        elif value == 'ascending_rating':
            expression = 'total_rating'
        elif value == 'descending_rating':
            expression = '-total_rating'
        elif value == 'descending_order':
            expression = '-quantity_of_purchases'
        return queryset.order_by(expression)

    def filter_by_price(self, queryset, name, value):
        if value == '10000':
            return queryset.filter(price__lte=10000)
        if value == '10001-30000':
            return queryset.filter(price__gt=10000, price__lte=30000)
        if value == '30001-50000':
            return queryset.filter(price__gt=30000, price__lte=50000)
        if value == '50001-70000':
            return queryset.filter(price__gt=50000, price__lte=70000)
        elif value == '70001':
            return queryset.filter(price__gt=70000)
