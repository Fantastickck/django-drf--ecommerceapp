
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import login, logout
from django.views import View
from django.views.generic import DetailView, UpdateView

from main.forms import EditProfileForm, UserLoginForm, UserRegisterForm

from .models import AdvUser, Profile



def home(request):
    return render(request, 'main/home.html')

def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Успешная регистрация')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else: 
        form = UserLoginForm()
    return render(request, 'main/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


class GetAdvUser(DetailView):
    model = Profile
    template_name = 'main/user.html'


# def edit_profile(request):
#     user = request.user
#     profile = get_object_or_404(Profile, user=user)
#     if request.method == 'POST':
#         form = EditProfileForm(request.POST, instance=profile)
#         if form.is_valid():
#             profile = form.save(commit=False)
#             profile.save()
#             return redirect('home')
#     else:
#         form = EditProfileForm(instance=profile)
#     return render(request, 'main/edit_profile.html', {'form': form})

class EditProfile(View):
    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        form = EditProfileForm(instance=profile)
        context = {
            'form': form
        }
        return render(request, 'main/edit_profile.html', context)

    def post(self, request):
        user = request.user
        form = EditProfileForm(request.POST)
        if form.is_valid():
            Profile.objects.update_or_create(user=user, defaults={**form.cleaned_data})
            return redirect('home')


    