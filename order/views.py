from django.shortcuts import render
from django.db.models import Q

from .models import Order, OrderItem
from .forms import OrderForm
from main.models import AdvUser, Profile
from cart.cart import Cart


# Возможно стоит переписать в вид контроллера-класса!!!
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            if request.user.is_authenticated:
                user = request.user
            order = Order.objects.create(
                user=user if request.user.is_authenticated else None,
                first_name=form_data['first_name'],
                last_name=form_data['last_name'],
                email=form_data['email'],
                phone=form_data['phone'],
                address=form_data['address'],
            )
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
            cart.clear()
            return render(request, 'order/created.html', {'order': order})
    else:
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            form = OrderForm()
            form = OrderForm(initial={
                'first_name': profile.first_name,
                'last_name': profile.last_name,
                'email': profile.user.email,
                'phone': profile.phone,
                'address': profile.default_address
            })
        else:
            form = OrderForm()
        return render(request, 'order/create.html', {'cart': cart, 'form': form})
