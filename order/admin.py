from django.contrib import admin

from order.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'first_name', 'last_name', 'email', 'address', 'created_date', 'paid']
    list_filter = ['paid', 'created_date']
    list_display_links = ['id']
    inlines = [
        OrderItemInline
    ]