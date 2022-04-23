import django_filters

from .models import Product

class ProductFilter(django_filters.FilterSet):

    CHOICES = (
        ('ascending', 'По возрастанию'),
        ('descending', 'По убыванию')
    )

    ordering = django_filters.ChoiceFilter(label='Сортировка', choices=CHOICES, method='filter_by_price')

    class Meta:
        model = Product
        fields = [
            'name',
            'brand'
        ]

    def filter_by_price(self, queryset, name, value):
        expression = 'price' if value == 'ascending' else '-price'
        return queryset.order_by(expression)