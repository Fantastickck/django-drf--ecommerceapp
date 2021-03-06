from django.shortcuts import render
from django.views.generic import View

from .models import Room
from main.models import AdvUser


class GetRoomsForAdmin(View):
    """
    Представление комнат для пользователей-админов
    """
    def get(self, request):
        user = request.user
        rooms = user.rooms.all()
        context = {
            'rooms': rooms,
        }
        return render(request, 'chat/get_rooms.html', context)


class GetRoom(View):
    """
    Представление списка сообщений из чата с админом
    """
    def get(self, request, id):
        user_admin = AdvUser.objects.get(id=1)
        room = Room.objects.get_or_create(id=id)[0]
        room.user.add(request.user.id)
        room.user.add(user_admin.id)
        messages = room.messages.all().order_by('created_at')
        context = {
            'room': room,
            'chat_messages': messages,
        }
        return render(request, 'chat/chat.html', context)
