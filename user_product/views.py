from django.shortcuts import render, redirect
from django.views.generic import ListView, View


from .models import Favourites, Order, OrderItem, Feedback, FeedbackImage, FavouritesItem
from .forms import OrderForm, FeedbackForm
from cart.forms import CartAddProductForm
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
            return render(request, 'user_product/created_order.html', {'order': order})
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
        return render(request, 'user_product/create_order.html', {'cart': cart, 'form': form})


class GetOrdersByUser(ListView):
    template_name = 'user_product/orders_by_user.html'
    context_object_name = 'orders'
    paginate_by = 3

    def get_queryset(self):
        orders = Order.objects.filter(user__profile__slug=self.kwargs['slug']).prefetch_related('items').prefetch_related('items__product')
        return orders


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
            product = Product.objects.get(id=product_id)
            feedback = Feedback.objects.create(
                user=request.user, product=product, text=data['text'], rating=data['rating'])
            product.save()
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


class GetFavourites(View):
    def get(self, request):
        favourites = Favourites.objects.get_or_create(user=self.request.user)[0]
        favourites_items = FavouritesItem.objects.filter(favourites=favourites).select_related('product')
        cart_product_form = CartAddProductForm()
        context = {
            'favourites': favourites,
            'favourites_items': favourites_items,
            'cart_product_form': cart_product_form 
        }
        return render(request, 'user_product/favourites.html', context)


class AddFavouritesItem(View):
    def get(self, request, product_id):
        favourites = Favourites.objects.get_or_create(user=self.request.user)[0]
        product = Product.objects.get(id=product_id)
        favourites_item = FavouritesItem.objects.get_or_create(favourites=favourites, product=product)
        return redirect('get_favourites')


class RemoveFavouritesItem(View):
    def get(self, request, item_id):
        favourites_item = FavouritesItem.objects.get(id=item_id)
        favourites_item.delete()
        return redirect('get_favourites')
        