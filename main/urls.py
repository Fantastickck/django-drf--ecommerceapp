from django.urls import path

from .views import EditProfile, GetAdvUser, home, user_register, user_login, user_logout

urlpatterns = [
    path('', home, name='home'),
    path('register/', user_register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('edit/', EditProfile.as_view(), name='edit_profile'),
    path('user/<slug:slug>/', GetAdvUser.as_view(), name='get_user'),

]
