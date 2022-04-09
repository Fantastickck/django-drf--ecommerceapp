from django.contrib import admin

from .models import Product, Category, Brand, Feature, Product_Feature

class ProductInline(admin.TabularInline):
    model = Product_Feature


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'count', 'category', 'brand')
    inlines = [
        ProductInline
    ]


class BrandInline(admin.TabularInline):
    model = Brand.category.through
    

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'info')
    inlines = [
        BrandInline
    ]

class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'info')
    

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand)
admin.site.register(Feature)
admin.site.register(Product_Feature)