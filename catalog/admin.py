from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Product, Category, Brand, Feature, Product_Feature

class ProductFeatureInline(admin.TabularInline):
    model = Product_Feature

class BrandInline(admin.TabularInline):
    model = Brand.category.through


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'count', 'image_show', 'category', 'brand')
    inlines = [
        ProductFeatureInline
    ]

    def image_show(self, obj):
        if obj.image:
            return mark_safe("<img src='{}' width='60' />".format(obj.image.url))
        return None

    image_show.__name__ = 'Миниатюра'
    
    
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
    list_display = ('name', 'logo_show','info')

    def logo_show(self, obj):
        if obj.logo:
            return mark_safe("<img src='{}' height='30' />".format(obj.logo.url))
        return None

    logo_show.__name__ = 'Лого'
    



admin.site.register(Feature)
admin.site.register(Product_Feature)