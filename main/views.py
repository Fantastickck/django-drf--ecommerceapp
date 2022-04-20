
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import login, logout
from django.views import View
from django.views.generic import DetailView, UpdateView, ListView
from django.views.decorators.csrf import csrf_protect

from main.forms import EditProfileForm, UserLoginForm, UserRegisterForm

from .models import AdvUser, Profile
from catalog.models import Product


def home(request):
    products = Product.objects.all().order_by('-quantity_of_purchases')[0:5]
    context = {
        'products': products
    }
    return render(request, 'main/home.html', context)


@csrf_protect
def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_id = AdvUser.objects.get(
                username=form.cleaned_data['username'])
            Profile.objects.create(
                user_id=user_id.id,
                slug=form.cleaned_data['username'].lower(),
                first_name='',
                last_name='',
                phone='',
                date_of_birth='2000-01-01',
                default_address='',
            )
            login(request, user)
            messages.success(request, 'Успешная регистрация')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        if request.user.is_authenticated:
            return render(request,'main/messages/already_auth.html')
        form = UserRegisterForm()
        context = {
            'form': form
        }
    return render(request, 'main/register.html', context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        if request.user.is_authenticated:
            return render(request,'main/messages/already_auth.html')
        form = UserLoginForm()
    context = {
        'form': form
    }
    return render(request, 'main/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('login')


class GetOrEditProfile(View):
    def get(self, request, slug):
        user = request.user
        profile = Profile.objects.get(user=user)
        form = EditProfileForm(instance=profile)
        context = {
            'form': form
        }
        return render(request, 'main/user.html', context)

    def post(self, request, slug):
        user = request.user
        form = EditProfileForm(request.POST)
        if form.is_valid():
            Profile.objects.update_or_create(
                user=user, defaults={**form.cleaned_data})
            return redirect('get_user', slug=slug)
