from django.shortcuts import redirect, render
from django.views.generic import View

from chat.forms import MessageForm

from .models import Message, Room
from main.models import AdvUser


class GetRoomsForAdmin(View):
    def get(self, request, id):
        user = request.user
        rooms = user.room_set.all()
        context = {
            'rooms': rooms,
        }
        return render(request, 'chat/get_rooms.html', context)


class GetRoom(View):
    def get(self, request, id):
        user_admin = AdvUser.objects.get(id=1)
        room = Room.objects.get_or_create(id=id)[0]
        room.user.add(request.user.id)
        room.user.add(user_admin.id)
        messages = room.messages.all().order_by('-created_at')[:5]
        form = MessageForm()
        context = {
            'room': room,
            'chat_messages': messages,
            'form': form,
        }
        return render(request, 'chat/chat.html', context)

    def post(self, request, id):
        form = MessageForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Message.objects.create(
                room=Room.objects.get(id=id),
                author=request.user,
                text=data['text'],
            )
            return redirect('get_room', id)

