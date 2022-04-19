from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import FeedbackImage, Product, Category, Brand, Feature, ProductFeature, Feedback


class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature


class BrandInline(admin.TabularInline):
    model = Brand.category.through


class FeedbackImageInline(admin.TabularInline):
    model = FeedbackImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity',
                    'image_show', 'category', 'brand', 'get_total_rating')
    inlines = [
        ProductFeatureInline
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
        BrandInline
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


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'text', 'rating', 'created_at')
    inlines = [
        FeedbackImageInline
    ]


admin.site.register(Feature)
admin.site.register(ProductFeature)
