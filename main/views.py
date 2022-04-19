
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import login, logout
from django.views import View
from django.views.generic import DetailView, UpdateView, ListView
from django.views.decorators.csrf import csrf_protect

from main.forms import EditProfileForm, UserLoginForm, UserRegisterForm

from .models import AdvUser, Profile

from order.models import Order, OrderItem


def home(request):
    return render(request, 'main/home.html')


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
        form = UserLoginForm()
    context = {
        'form': form
    }
    return render(request, 'main/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('login')


class GetOrdersByUser(ListView):
    model = Order
    template_name = 'main/orders_by_user.html'
    context_object_name = 'orders'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     orders = Order.objects.filter(user__profile__slug=self.kwargs['slug'])
    #     context['items_by_orders'] = {

    #     }

    def get_queryset(self):
        return Order.objects.filter(user__profile__slug=self.kwargs['slug'])

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
            return redirect('home')
