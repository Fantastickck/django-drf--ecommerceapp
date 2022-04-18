from django.urls import path

from .views import GetOrdersByUser, home, user_register, user_login, user_logout, GetOrEditProfile

urlpatterns = [
    path('', home, name='home'),
    path('register/', user_register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('user/orders/<slug:slug>', GetOrdersByUser.as_view(), name='get_orders'),
    path('user/profile/<slug:slug>/', GetOrEditProfile.as_view(), name='get_user')
]
