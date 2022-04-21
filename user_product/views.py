from django.shortcuts import render, redirect
from django.db.models import Q
from django.views.generic import ListView, View


from .models import Order, OrderItem, Feedback, FeedbackImage
from .forms import OrderForm, FeedbackForm
from main.models import AdvUser, Profile
from cart.cart import Cart
from catalog.models import Product


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
                product = Product.objects.get(name=item['product'])
                product.quantity -= item['quantity']
                product.quantity_of_purchases += item['quantity']
                product.save()
            cart.clear()
            return render(request, 'user_product/created.html', {'order': order})
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
        return render(request, 'user_product/create.html', {'cart': cart, 'form': form})


class GetOrdersByUser(ListView):
    model = Order
    template_name = 'user_product/orders_by_user.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user__profile__slug=self.kwargs['slug'])


class CreateFeedback(View):
    def get(self, request, product_id):
        feedback_exist = Feedback.objects.filter(user=self.request.user, product=self.kwargs['product_id']).exists()
        if feedback_exist:
            prev_url = request.META.get('HTTP_REFER')
            return render(request, 'user_product/messages/already_created.html', {'prev_url': prev_url})
        product = Product.objects.get(id=product_id)
        form = FeedbackForm()
        context = {
            'form': form,
            'product': product,
        }
        return render(request, 'user_product/create_feedback.html', context)

    def post(self, request, product_id):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            feedback = Feedback.objects.create(
                user=request.user, product_id=product_id, text=data['text'], rating=data['rating'])
            for file in request.FILES.getlist('images'):
                image = FeedbackImage.objects.create(
                    feedback=feedback, image=file)
            return redirect('get_product', product_id=product_id)

class RemoveFeedback(View):
    def get(self, request, feedback_id):
        feedback = Feedback.objects.get(id=feedback_id)
        product_id = feedback.product.id
        feedback.delete()
        return redirect('get_product', product_id)