from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Product, Category, Brand, Feature, ProductFeature, ProductImage


class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature


class BrandInline(admin.TabularInline):
    model = Brand.category.through

class ProductImageInline(admin.TabularInline):
    model = ProductImage



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'quantity_of_purchases',
                    'image_show', 'category', 'brand', 'get_total_rating')
    inlines = [
        ProductImageInline,
        ProductFeatureInline,
    ]

    def image_show(self, obj):
        if obj.image:
            return mark_safe("<img src='{}' width='60' />".format(obj.image.url))
        return None

    image_show.short_description = 'Миниатюра'
    Product.get_total_rating.short_description = 'Рейтинг'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo_show', 'info')
    inlines = [
        BrandInline,
    ]

    def logo_show(self, obj):
        if obj.logo:
            return mark_safe("<img src='{}' width='60' />".format(obj.logo.url))
        return None

    logo_show.__name__ = 'Лого'


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo_show', 'info')

    def logo_show(self, obj):
        if obj.logo:
            return mark_safe("<img src='{}' height='30' />".format(obj.logo.url))
        return None

    logo_show.__name__ = 'Лого'





admin.site.register(Feature)
admin.site.register(ProductFeature)
