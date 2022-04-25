from django.urls import path

from .views import home, user_register, user_login, user_logout, GetOrEditProfile, ChangePassword

urlpatterns = [
    path('', home, name='home'),
    path('register/', user_register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('user/change/password/', ChangePassword.as_view(), name='change_password'),
    path('user/profile/<slug:slug>/', GetOrEditProfile.as_view(), name='get_user')
]
