import django_filters

from .models import Product

class ProductFilter(django_filters.FilterSet):

    CHOICES = (
        ('ascending_price', 'По возрастанию цены'),
        ('descending_price', 'По убыванию цены'),
        ('ascending_rating', 'По возрастанию рейтинга'),
        ('descending_rating', 'По убыванию рейтинга'),
    )

    ordering = django_filters.ChoiceFilter(label='Сортировка', choices=CHOICES, method='filter')

    class Meta:
        model = Product
        fields = [
            'brand',
        ]
    

    def filter(self, queryset, name, value):
        expression = ''
        if value == 'ascending_price':
            expression = 'price'
        elif value == 'descending_price':
            expression = '-price'
        elif value == 'ascending_rating':
            expression = 'total_rating'
        elif value == 'descending_rating':
            expression = '-total_rating'
        return queryset.order_by(expression)
    