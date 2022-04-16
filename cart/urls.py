from django.urls import path, include
from django.conf.urls import url

from .views import cart_add, cart_detail, cart_remove


urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    # url(r'^$', cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', cart_add, name='cart_add'),
    path('remove/<int:product_id>/', cart_remove, name='cart_remove'),
]
