from django.contrib import admin

from .models import Product, Category, Brand, Feature, Product_Feature


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Feature)
admin.site.register(Product_Feature)