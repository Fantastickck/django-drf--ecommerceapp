import re
from django.shortcuts import render

from .models import Order, OrderItem
from .forms import OrderForm
from main.models import AdvUser
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            if request.user:
                user = request.user
            form_data = form.cleaned_data
            order = Order.objects.create(
                user=user,
                first_name=form_data['first_name'],
                last_name=form_data['last_name'],
                email=form_data['email'],
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
        form = OrderForm()
    return render(request, 'order/create.html', {'cart': cart, 'form': form})
