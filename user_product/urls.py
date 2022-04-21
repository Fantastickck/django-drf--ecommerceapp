from django.urls import path

from .views import RemoveFeedback, order_create, GetOrdersByUser, CreateFeedback

urlpatterns = [
    path('create-order/', order_create, name='order_create'),
    path('user/orders/<slug:slug>', GetOrdersByUser.as_view(), name='get_orders'),
    path('create_feedback/<int:product_id>/',
         CreateFeedback.as_view(), name='create_feedback'),
    path('delete_feedback/<int:feedback_id>', RemoveFeedback.as_view(), name='remove_feedback')
]
