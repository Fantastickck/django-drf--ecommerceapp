
from ast import Pass
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import PasswordChangeView, PasswordContextMixin
from django.views import View
from django.views.generic import DetailView, UpdateView, ListView
from django.views.decorators.csrf import csrf_protect

from main.forms import ChangePasswordForm, EditProfileForm, UserLoginForm, UserRegisterForm
from cart.forms import CartAddProductForm

from .models import AdvUser, Profile
from catalog.models import Product


def home(request):
    products = Product.objects.all().order_by('-quantity_of_purchases')[0:5].prefetch_related('feedbacks')
    context = {
        'products': products,
        'cart_product_form': CartAddProductForm,
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
            return render(request, 'main/messages/already_auth.html')
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
            messages.success(request, 'Успешный вход')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка входа')
    else:
        if request.user.is_authenticated:
            return render(request, 'main/messages/already_auth.html')
        form = UserLoginForm()
    context = {
        'form': form
    }
    return render(request, 'main/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('login_app')


class ChangePassword(View):
    def get(self, request):
        form = ChangePasswordForm()
        prev_url = request.META.get('HTTP_REFERER')
        context = {
            'form': form,
            'prev_url': prev_url,
        }
        return render(request, 'main/change_password.html', context)

    def post(self, request):
        user = AdvUser.objects.get(id=request.user.id)
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            old_password = data['old_password']
            new_password = data['new_password']
            new_password_again = data['new_password_again']
            if user.check_password(old_password):
                if new_password == new_password_again:
                    print(old_password, new_password)
                    user.set_password(new_password)
                    user.save()

                else:

                    messages.error(request, 'Введенные пароль не совпадают')
                    return redirect('change_password')
            else:
                messages.error(request, 'Неправильный пароль')
                return redirect('change_password')

            logout(request)
            return redirect('login')


class GetOrEditProfile(View):
    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        form = EditProfileForm(instance=profile)
        context = {
            'form': form,
            'profile': profile
        }
        return render(request, 'main/user.html', context)

    def post(self, request):
        user = request.user
        form = EditProfileForm(request.POST)
        if form.is_valid():
            Profile.objects.update_or_create(
                user=user, defaults={**form.cleaned_data})
            return redirect('get_user')
