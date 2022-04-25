from django.contrib import admin

from .models import Room, Message

class MessageInline(admin.TabularInline):
    model = Message

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['id']
    inlines = [
        MessageInline
    ]