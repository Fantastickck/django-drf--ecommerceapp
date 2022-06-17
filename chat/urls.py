from django.urls import path

from .views import GetRoom, GetRoomsForAdmin

urlpatterns = [
    path('<int:id>/', GetRoom.as_view(), name='get_room'),
    path('rooms/', GetRoomsForAdmin.as_view(), name='get_rooms_for_admin')
]
