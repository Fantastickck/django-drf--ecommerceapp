from django.contrib import admin

from .models import Order, OrderItem, Feedback, FeedbackImage


class OrderItemInline(admin.TabularInline):
    model = OrderItem

class FeedbackImageInline(admin.TabularInline):
    model = FeedbackImage

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'first_name', 'last_name', 'email', 'address', 'created_date', 'paid']
    list_filter = ['paid', 'created_date']
    list_display_links = ['id']
    inlines = [
        OrderItemInline
    ]


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'text', 'rating', 'created_at')
    inlines = [
        FeedbackImageInline
    ]