from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Product, Category, Brand, Feature, ProductFeature, ProductImage


class ProductFeatureInline(admin.TabularInline):
    """
    Список характеристик товара.
    """
    model = ProductFeature

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('feature', 'product')


class BrandInline(admin.TabularInline):
    """
    Список брендов.
    """
    model = Brand.category.through


class ProductImageInline(admin.TabularInline):
    """
    Список фото товара
    """
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'quantity_of_purchases',
                    'image_show', 'category', 'brand', 'total_rating')

    inlines = [
        ProductImageInline,
        ProductFeatureInline,
    ]

    list_select_related = ['features']

    def image_show(self, obj):
        """Изображение товара в админке в виде миниатюры."""
        if obj.image:
            return mark_safe("<img src='{}' width='60' />".format(obj.image.url))
        return None

    image_show.short_description = 'Миниатюра'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo_show', 'info')
    inlines = [
        BrandInline,
    ]

    def logo_show(self, obj):
        """Лого категории в админке в виде миниатюры."""
        if obj.logo:
            return mark_safe("<img src='{}' width='60' />".format(obj.logo.url))
        return None

    logo_show.__name__ = 'Лого'


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo_show', 'info')

    def logo_show(self, obj):
        """Лого бренда в админке в виде миниатюры."""
        if obj.logo:
            return mark_safe("<img src='{}' height='30' />".format(obj.logo.url))
        return None

    logo_show.__name__ = 'Лого'


admin.site.register(Feature)
admin.site.register(ProductFeature)
admin.site.register(ProductImage)
