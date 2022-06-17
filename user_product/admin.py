from django.contrib import admin

from .models import Order, OrderItem, Feedback, FeedbackImage, Favourites, FavouritesItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem


class FeedbackImageInline(admin.TabularInline):
    model = FeedbackImage


class FavouritesItemInline(admin.TabularInline):
    model = FavouritesItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name',
                    'email', 'address', 'created_date', 'get_total_cost', 'paid']
    list_filter = ['paid', 'created_date']
    list_display_links = ['id']
    inlines = [
        OrderItemInline
    ]


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'text', 'rating', 'created_at']
    inlines = [
        FeedbackImageInline
    ]


@admin.register(Favourites)
class Favourites(admin.ModelAdmin):
    list_display = ['user']
    inlines = [
        FavouritesItemInline
    ]
